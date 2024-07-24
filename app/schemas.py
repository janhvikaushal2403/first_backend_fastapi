from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    # optional field
    published: bool = True 
    # fully optional field
    # rating: Optional[int] = None    removing for now while creating a table

class PostCreate(PostBase):
    pass

# response model for user, add here becoz we used in post so need to declare before 
class UserOut(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

  class Config:
      orm_mode = True

# response model 
# inheriting the postbase class
class Post(PostBase):
    id: int 
    created_at: datetime
    owner_id : int 
    owner : UserOut

    class Config:
        orm_mode = True

class PostOut(PostBase):
    created_at: datetime
    owner_id: int
    published : bool

    owner : UserOut
    votes : int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# response model for user
class UserLogin(BaseModel):
   email: EmailStr
   password: str

class Token(BaseModel):
    access_token: str
    token_type: str   

class TokenData(BaseModel):
    id: Optional[int] = None
    # id: int

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)    # type: ignore