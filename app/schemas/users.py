from pydantic import BaseModel
from datetime import datetime

class UserFullData(BaseModel):
    id : int
    username : str
    password : str 
    created_at : datetime
    updated_at : datetime 
    
    
class UserFullDataWithoutPassword(BaseModel):
    id : int
    username : str
    created_at : datetime
    updated_at : datetime 
    

class UserFormFront(BaseModel):
    username : str
    password : str
    