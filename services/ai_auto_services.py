import os
import re
import traceback
import requests
import google.generativeai as genai
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from models.blog_post import BlogPost
from crud.crud_blog_post import crud_blog_post
from schemas.blog_post import BlogPostCreate
from crud.crud_ai_prompt import crud_ai_prompt
from models.ai_prompt import AIPrompt
import markdown as md

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
print("\U0001f511 Gemini API Key loaded from .env:", os.getenv("GEMINI_API_KEY"))


def extract_keywords_from_topic(topic: str) -> tuple[str, list]:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    From this topic: \"{topic}\", generate:
    - 1 best focus keyword
    - 3–5 secondary keywords (comma-separated)

    Format:
    focus Keyword: <keyword>
    Secondary Keywords: <kw1>, <kw2>, <kw3>, ...
    """
    result = model.generate_content(prompt).text
    lines = result.splitlines()
    focus = ""
    secondary = []
    for line in lines:
        if line.startswith("focus Keyword:"):
            focus = line.split(":")[1].strip()
        if line.startswith("Secondary Keywords:"):
            secondary = [x.strip() for x in line.split(":")[1].split(",")]
    return focus, secondary


def generate_blog_post_content(
    db: Session, topic: str, prompt_id: int = None
) -> BlogPost:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Get keywords
        focus, secondary = extract_keywords_from_topic(topic)
        print(f"Focus Keyword: {focus}")
        print(f"Secondary Keywords: {secondary}")
        keywords_str = ", ".join([focus] + secondary)

        # Load prompt from DB
        if prompt_id:
            prompt_obj = db.query(AIPrompt).filter(AIPrompt.id == prompt_id).first()
        else:
            prompt_obj = crud_ai_prompt.get_latest(db)

        if not prompt_obj:
            raise ValueError("No valid prompt found in DB")

        # Replace variables in prompt
        user_prompt = (
            prompt_obj.prompt.replace("{topic}", topic)
            .replace("{focus_keyword}", focus)
            .replace("{secondary_keywords}", ", ".join(secondary))
        )

        # Generate blog
        response = model.generate_content(user_prompt)
        full_text = response.text.strip()
        print("Generated Blog Content:\n", full_text)

        # Extract meta fields and remove them
        meta_title_match = re.search(
            r"meta title:\s*(.*?)</p>", full_text, re.IGNORECASE
        )
        meta_description_match = re.search(
            r"meta description:\s*(.*?)</p>", full_text, re.IGNORECASE
        )
        meta_title = meta_title_match.group(1).strip() if meta_title_match else ""
        meta_description = (
            meta_description_match.group(1).strip() if meta_description_match else ""
        )

        full_text = re.sub(r"<p>meta title:.*?</p>", "", full_text, flags=re.IGNORECASE)
        full_text = re.sub(
            r"<p>meta description:.*?</p>", "", full_text, flags=re.IGNORECASE
        )
        full_text = re.sub(r"<p>blog slug:.*?</p>", "", full_text, flags=re.IGNORECASE)

        # Extract title from <h1>
        title_match = re.search(r"<h1>(.*?)</h1>", full_text, re.IGNORECASE)
        title = title_match.group(1).strip().title() if title_match else "Untitled Blog"
        content = re.sub(
            r"<h1>.*?</h1>", "", full_text, count=1, flags=re.IGNORECASE
        ).strip()

        # Capitalize first letters in <p> and justify
        content = re.sub(
            r"<p>(.*?)</p>",
            lambda m: f'<p style="text-align: justify;"><strong>{m.group(1).strip().capitalize()}</strong></p>',
            content,
            flags=re.IGNORECASE,
        )

        blog_data = {
            "topic": topic,
            "title": title,
            "content": content,
            "keywords": keywords_str,
            "status": "pending",
        }

        return crud_blog_post.create(db, obj_in=blog_data)

    except Exception as e:
        traceback.print_exc()
        raise RuntimeError(f"Failed to generate blog post: {str(e)}")


def publish_post_to_wordpress(db: Session, post_id: int) -> BlogPost:
    post = crud_blog_post.get(db, id=post_id)
    if not post:
        raise ValueError("Post not found")

    WORDPRESS_URL = os.getenv("WORDPRESS_URL")
    WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
    WORDPRESS_APP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD")

    if not WORDPRESS_URL or not WORDPRESS_USERNAME or not WORDPRESS_APP_PASSWORD:
        raise ValueError("WordPress credentials missing in .env")

    payload = {
        "title": post.title,
        "content": post.content,
        "status": "draft",  # 👈 Save as draft
    }

    print(WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD, WORDPRESS_URL)
    auth = HTTPBasicAuth(WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD)
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"

    response = requests.post(url, json=payload, auth=auth)

    if response.status_code == 201:
        wp_data = response.json()
        post.wordpress_id = wp_data["id"]
        post.status = "draft"  # 👈 Store local status as draft
        db.commit()
        db.refresh(post)
        return post
    else:
        post.status = "failed"
        db.commit()
        try:
            error_detail = response.json()
        except:
            error_detail = response.text
        raise Exception(
            f"WordPress publish failed: {response.status_code} {error_detail}"
        )


def analyze_for_ai_detection(db: Session, post_id: int) -> BlogPost:
    post = crud_blog_post.get(db, id=post_id)
    if not post:
        raise ValueError("Post not found")

    score = 30 if "AI" in post.title else 80
    post.is_ai_detected = score > 50
    post.ai_detection_score = score
    db.commit()
    db.refresh(post)
    return post
