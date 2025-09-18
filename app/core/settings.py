from pydantic_settings import BaseSettings


class MySetting(BaseSettings):
    DATA_BASE_URL : str
    
    SECRET_KEY : str 
    EXPIRE_TOKEN_MINUTES : int
    ALGORITHM : str
    
    class Config:
        env_file = ".env"
    
my_settings = MySetting() # type: ignore


