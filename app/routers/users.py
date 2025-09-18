from fastapi import APIRouter, status, Depends, Body, HTTPException, Path, Form
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.users import UserFullData, UserFullDataWithoutPassword, UserFormFront
from app.models.user import User
from typing import Annotated
from app.schemas.tokens import TokenHeader, TokenDataForCreate
from app.utils.passwords_service import hash_pw, verify_pw
from app.core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.core.logger import logger


router = APIRouter(
    prefix='/users',
    tags=['Auth']
)

#====================================================#
#============  Create a New USER                              
#====================================================#
@router.post('/register', response_model=UserFullDataWithoutPassword, status_code=status.HTTP_201_CREATED)
def register(
    db: Annotated[Session, Depends(get_db)],
    user_input: Annotated[UserFormFront, Body(..., description='inputs for create a new user.')]
):
    existing_user = db.query(User).filter(User.username == user_input.username).first()
    
    if existing_user:
        logger.warning(f'Someone tried to create new account but the username was already taken.')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Username <{user_input.username}> already taken!'
        )
    
    # hash the pw:
    user_input_dict = user_input.model_dump()
    user_input_dict['password'] = hash_pw(user_input_dict['password'])
    
    new_user = User(**user_input_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f'New account created => User ID<{new_user.id}>.')
    return new_user



#====================================================#
#============  Login                              
#====================================================#
@router.post('/login', status_code=status.HTTP_200_OK, response_model=TokenHeader)
def login(
    db: Annotated[Session, Depends(get_db)],
    user_input: Annotated[OAuth2PasswordRequestForm, Depends()]
    
):
    user = db.query(User).filter(User.username == user_input.username).first()
    
    if user is None or not verify_pw(user_input.password, user.password):
        logger.warning('Someone tried to login but get Invalds Credential.')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Credentials',
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    token_data = TokenDataForCreate(sub=user.username)
    token = create_access_token(token_data)
    logger.info(f'Token created for User ID<{user.id}>.')
    
    return TokenHeader(access_token=token)
    
    