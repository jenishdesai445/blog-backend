from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class AIPromptBase(BaseModel):
    prompt: str


class AIPromptCreate(AIPromptBase):
    pass


class AIPromptResponse(AIPromptBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AIPromptUpdate(BaseModel):
    prompt: Optional[str] = None
