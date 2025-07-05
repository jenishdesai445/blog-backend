from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api.dependencies import get_db
from schemas.blog_post import BlogPostCreate, BlogPostResponse
from services.ai_auto_services import (
    generate_blog_post_content,
    publish_post_to_wordpress,
    analyze_for_ai_detection
)
from crud.crud_blog_post import crud_blog_post
from models.blog_post import BlogPost

router = APIRouter()

@router.post("/posts/", response_model=BlogPostResponse, status_code=status.HTTP_201_CREATED)
async def create_new_blog_post(
    post: BlogPostCreate,
    db: Session = Depends(get_db)
):
    try:
        new_post = generate_blog_post_content(
            db=db,
            topic=post.topic,
            prompt_id=post.prompt_id
        )
        return new_post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to generate post: {e}")



@router.get("/posts/", response_model=List[BlogPostResponse], tags=["WordPress Automation"])
async def get_all_blog_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieves a list of all blog posts from the database.
    Public access (no authentication).
    """
    posts = crud_blog_post.get_multi(db, skip=skip, limit=limit)
    return posts


@router.get("/posts/{post_id}", response_model=BlogPostResponse, tags=["WordPress Automation"])
async def get_blog_post_by_id(
    post_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves a single blog post by its ID.
    Public access (no authentication).
    """
    post = crud_blog_post.get(db, id=post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post



@router.post("/posts/{post_id}/publish", response_model=BlogPostResponse, tags=["WordPress Automation"])
async def publish_blog_post_endpoint(
    post_id: int,
    db: Session = Depends(get_db)
):
    """
    Publishes a generated blog post to WordPress.
    Public access (no authentication).
    """
    try:
        updated_post = publish_post_to_wordpress(db, post_id)
        return updated_post
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        if "401" in str(e):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="❌ Unauthorized: Check WordPress credentials or user role (must be admin)."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to publish post: {e}"
        )

@router.post("/posts/{post_id}/detect_ai", response_model=BlogPostResponse, tags=["WordPress Automation"])
async def run_ai_detection_endpoint(
    post_id: int,
    db: Session = Depends(get_db)
):
    """
    Runs AI content detection on a generated blog post.
    Public access (no authentication).
    """
    try:
        updated_post = analyze_for_ai_detection(db, post_id)
        return updated_post
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to run AI detection: {e}")
