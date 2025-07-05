from bs4 import BeautifulSoup
import re

def capitalize_html_content(html: str, mode: str = "auto") -> str:
    """
    Processes HTML to:
    - Capitalize content by tag
    - Bold key terms
    - Justify <p> tags
    - Keep clean line breaks
    """

    soup = BeautifulSoup(html, "html.parser")

    # Bold important keywords (extend as needed)
    bold_keywords = [
        "ai", "artificial intelligence", "automation", "intelligent automation",
        "business", "software", "productivity", "cost", "customer", "data"
    ]

    def bold_keywords_in_text(text):
        for kw in sorted(bold_keywords, key=len, reverse=True):
            pattern = re.compile(rf"(?<!<strong>)(\b{re.escape(kw)}\b)(?!</strong>)", re.IGNORECASE)
            text = pattern.sub(r"<strong>\1</strong>", text)
        return text

    def sentence_case(text):
        return ". ".join(s.strip().capitalize() for s in text.split(". "))

    def title_case(text):
        return text.title()

    for tag in soup.find_all(["p", "h1", "h2", "h3", "li"]):
        if tag.string:
            txt = tag.string.strip()
            if tag.name in ["h1", "h2", "h3"]:
                tag.string = title_case(txt)
            else:
                tag.string = sentence_case(txt)

        # Apply justification to <p>
        if tag.name == "p":
            tag["style"] = "text-align: justify;"

        # Bold key terms inside tag content
        if tag.string:
            tag.clear()
            tag.append(BeautifulSoup(bold_keywords_in_text(tag.text), "html.parser"))

    return str(soup)
