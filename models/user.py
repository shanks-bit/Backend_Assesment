from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from bson import ObjectId
import datetime

class PostModel(BaseModel):
    post_id: int
    text: str
    image: Optional[str] = None
    hashtags: List[str]

class UpdatePostModel(BaseModel):
    post_id: int = None
    text: str = None
    image: Optional[str] = None
    hashtags: List[str] = None

class UserModel(BaseModel):
    user_id: int
    name: str
    mobile_no: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    posts: list[PostModel] | None = None


class UpdateUserModel(BaseModel):
    user_id: int = None
    name: str = None
    mobile_no: str = None
    email: EmailStr = None
    posts: list[PostModel] = None

    

