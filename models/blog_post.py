# models/blog_post.py
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.types import DateTime, SmallInteger
from sqlalchemy.sql import func
from db.base_class import Base # Assuming Base is defined in db/base_class.py

class BlogPost(Base): # Inherit from your Base class
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    keywords = Column(String) # Comma-separated keywords
    status = Column(String, default="draft", nullable=False) # e.g., 'draft', 'generated', 'published', 'failed'
    wordpress_id = Column(Integer, unique=True, nullable=True) # ID of the post in WordPress
    is_ai_detected = Column(Boolean, default=False)
    ai_detection_score = Column(Integer, nullable=True) # e.g., percentage score if available
    # ✅ New fields must exist here:
    # length_words = Column(Integer, nullable=True)
    # primary_keyword = Column(String, nullable=True)
    # secondary_keywords = Column(String, nullable=True)
    
    
    created_by = Column(String, nullable=True) 

    # `created_date`, `modified_date`, `status` are already handled by your Base class.
    # No need to redefine them here if your Base includes them.

    # Example of how to use existing Base columns:
    # created_date = Column(DateTime(timezone=True), server_default=func.now())
    # modified_date = Column(DateTime(timezone=True), onupdate=func.now())
    # status = Column(SmallInteger , nullable=False, default=1) # Your status column