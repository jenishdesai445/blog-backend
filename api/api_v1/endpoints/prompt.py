from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.dependencies import get_db
from schemas.ai_prompt import AIPromptCreate, AIPromptResponse, AIPromptUpdate
from crud.crud_ai_prompt import crud_ai_prompt

router = APIRouter()


@router.post("/prompt/")
def create_prompt(prompt: AIPromptCreate, db: Session = Depends(get_db)):
    return crud_ai_prompt.create(db, obj_in=prompt)


@router.get("/prompt/latest")
def get_latest_prompt(db: Session = Depends(get_db)):
    prompt = crud_ai_prompt.get_latest(db)
    if not prompt:
        raise HTTPException(status_code=404, detail="No prompt found")
    return prompt


@router.put("/prompt/{prompt_id}")
def update_prompt(
    prompt_id: int,
    prompt_update: AIPromptUpdate,
    db: Session = Depends(get_db),
):
    prompt = crud_ai_prompt.get(db, id=prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return crud_ai_prompt.update(db=db, db_obj=prompt, obj_in=prompt_update)
