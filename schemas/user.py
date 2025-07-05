from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
   
    email: EmailStr
    password: str
    

class UserBase(BaseModel):

    email: Optional[EmailStr] = None
    password: Optional[str] = None
    status: int = 1


class UserCreate(UserBase):
    email: EmailStr
    status: int = 1
    class Config:
        orm_mode = True

class UserDetails(UserBase):
    
    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    id: int


class UserDelete(UserBase):
    id: int


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserOnly(UserInDBBase):
    ...


class UserSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool

