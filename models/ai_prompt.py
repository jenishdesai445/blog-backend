# ✅ models/ai_prompt.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from db.base_class import Base

class AIPrompt(Base):
    __tablename__ = "ai_prompts"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
