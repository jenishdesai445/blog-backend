# crud/crud_blog_post.py
from crud.base import CRUDBase
from models.blog_post import BlogPost
from schemas.blog_post import BlogPostCreate, BlogPostUpdate

class CRUDBlogPost(CRUDBase[BlogPost, BlogPostCreate, BlogPostUpdate]):
    pass # All necessary CRUD operations are inherited from CRUDBase

crud_blog_post = CRUDBlogPost(BlogPost)