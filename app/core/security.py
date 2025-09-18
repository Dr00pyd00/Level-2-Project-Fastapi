# import jwt
from app.core.settings import my_settings
from app.schemas.tokens import TokenDataForCreate
from datetime import timedelta, timezone ,datetime
from fastapi import HTTPException, status, Depends
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.schemas.users import UserFullDataWithoutPassword
from jose import JWTError, jwt

#====================================================#
#============  Utils                            
#====================================================#
cred_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalids Credential hihi',
    headers={"WWW-Authenticate": "Bearer"},
)

# For get the token etc in the header automatic:
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')



#====================================================#
#============  Create Access token                              
#====================================================#
def create_access_token(data:TokenDataForCreate) -> str:

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=my_settings.EXPIRE_TOKEN_MINUTES)
    
    to_encode = data.model_dump()
    to_encode.update({
        'exp': expire,
        'iat': now
        })
  
    
    token = jwt.encode(
        claims=to_encode,
        key=my_settings.SECRET_KEY,
        algorithm=my_settings.ALGORITHM
    )

    return token


#====================================================#
#============  Verify Token : and get user ID                              
#====================================================#
def verify_token(token:str) -> int:
    
    try:

        payload = jwt.decode(
            token=token,
            key=my_settings.SECRET_KEY,
            algorithms=[my_settings.ALGORITHM]
            
            )
        user_username = payload.get('sub')

        if user_username is None:
            raise cred_error
    
        return user_username
        
    except JWTError:
        raise cred_error
    

#====================================================#
#============  Get Current User                               
#====================================================#
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    
    ) -> User:
    
    print(f'func get_current_user token: {token} ')
    user_username = verify_token(token=token)
    
    current_user = db.query(User).filter(User.username == user_username).first()
    if current_user is None:
        raise cred_error
    
    return current_user

    