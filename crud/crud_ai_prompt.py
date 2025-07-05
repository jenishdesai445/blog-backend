from crud.base import CRUDBase
from models.ai_prompt import AIPrompt
from schemas.ai_prompt import AIPromptCreate
from sqlalchemy.orm import Session


class CRUDAIPrompt(CRUDBase[AIPrompt, AIPromptCreate, AIPromptCreate]):
    def get_latest(self, db: Session):
        return db.query(AIPrompt).all()


crud_ai_prompt = CRUDAIPrompt(AIPrompt)
