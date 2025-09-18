from pydantic import BaseModel
from datetime import datetime
from app.schemas.users import UserFullDataWithoutPassword


class PostFormFront(BaseModel):
    title : str
    content : str
    
class PostUpdateFront(BaseModel):
    title : str | None = None
    content : str | None = None
    
class PostFullData(BaseModel):
    id : int
    title : str
    content : str
    created_at : datetime
    updated_at : datetime
    user_id : int
    user : UserFullDataWithoutPassword
    likes_count : int
    
    class Config:
        from_attributes = True

    
    