# # schemas/blog_post.py
# # ✅ Updated schemas/blog_post.py to accept only topic
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class BlogPostBase(BaseModel):
    topic: str
    # length_words, primary_keyword, and secondary_keywords removed from user input

class BlogPostCreate(BlogPostBase):
    prompt_id: Optional[int] = None  # ✅ Optional, allows user to choose saved prompt

class BlogPostUpdate(BlogPostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    keywords: Optional[str] = None
    status: Optional[str] = None
    wordpress_id: Optional[int] = None
    is_ai_detected: Optional[bool] = None
    ai_detection_score: Optional[int] = None

class BlogPostResponse(BlogPostBase):
    id: int
    title: str
    content: str
    keywords: Optional[str] = None
    status: str
    wordpress_id: Optional[int] = None
    created_date: datetime
    modified_date: Optional[datetime] = None
    is_ai_detected: bool
    ai_detection_score: Optional[int] = None

    class Config:
        from_attributes = True







# from pydantic import BaseModel, validator
# from datetime import datetime
# from typing import Optional, List

# class BlogPostBase(BaseModel):
#     topic: str
#     length_words: Optional[int] = 700
#     primary_keyword: Optional[str] = None
#     secondary_keywords: Optional[List[str]] = None
#     @validator("secondary_keywords", pre=True)
#     def split_secondary_keywords(cls, v):
#         if isinstance(v, str):
#             return [s.strip() for s in v.split(",")]
#         return v

# class BlogPostCreate(BlogPostBase):
#     pass # For creation, we just need the base fields

# class BlogPostUpdate(BlogPostBase):
#     title: Optional[str] = None
#     content: Optional[str] = None
#     keywords: Optional[str] = None
#     status: Optional[str] = None
#     wordpress_id: Optional[int] = None
#     is_ai_detected: Optional[bool] = None
#     ai_detection_score: Optional[int] = None

# class BlogPostResponse(BlogPostBase):
#     id: int
#     title: str
#     content: str
#     keywords: Optional[str] = None
#     status: str
#     wordpress_id: Optional[int] = None
#     created_date: datetime # From your Base class
#     modified_date: Optional[datetime] = None # From your Base class
#     is_ai_detected: bool
#     ai_detection_score: Optional[int] = None

#     class Config:
#         from_attributes = True # For Pydantic v2
#         # or `orm_mode = True` for Pydantic v1.
#         # It allows Pydantic to read ORM models.