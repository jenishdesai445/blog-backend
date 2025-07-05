from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
#from models.user import User
from sqlalchemy.orm import Session
from db.base_class import Base
#from schemas.user import UserSearch

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()
    
    
    def get_multi(
        self, db: Session, *, skip: int=0, limit: int=100,
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()    
 
    # def get_sub_cate_multi(
    #     self, db: Session, *, skip: int = 0, limit: int = 100, category_id : int
    # ) -> List[ModelType]:
        
    #     return db.query(self.model).filter(SubCategorys.category_id == category_id).offset(skip).limit(limit).all()    

   
    
    # def get_category_multi(
    #     self, db: Session, *, skip: int = 0, limit: int = 100,
    # ) -> List[ModelType]:
    #     return db.query(self.model).offset(skip).limit(limit).all()

    # def get_multi_with_filter(
    #     self, db: Session, filter_tpl=None, skip: int = 0, limit: int = 100,
    # ) -> List[ModelType]:
    #     if filter_tpl is None:
    #         return db.query(self.model).filter(User.is_super_admin == False).filter(self.model.status == 1).offset(skip).limit(limit).all()
    #     else:
    #         return db.query(self.model).filter(User.is_super_admin == False,self.model.status == 1, filter_tpl).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType, created_by=None) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        # obj_in_data["created_by"] = created_by
        db_obj = self.model(**obj_in_data)  
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        modified_by=None
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        update_data["modified_by"] = modified_by
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
    






