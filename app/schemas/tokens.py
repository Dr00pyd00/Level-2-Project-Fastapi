from pydantic import BaseModel


class TokenDataForCreate(BaseModel):
    sub : str



class TokenHeader(BaseModel):
    access_token : str
    token_type : str = 'bearer'
    