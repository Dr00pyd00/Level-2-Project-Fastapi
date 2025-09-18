from fastapi import APIRouter, status, Depends, Body, HTTPException, Path, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.posts import PostFullData, PostFormFront, PostUpdateFront
from app.models.post import Post
from app.models.like import Like
from typing import Annotated
from app.core.security import get_current_user
from app.models.user import User
from app.core.logger import logger
from app.utils import logger_messages

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


#====================================================#
#============  Get all Posts                              
#====================================================#
@router.get('/', response_model=list[PostFullData], status_code=status.HTTP_200_OK)
def get_all_post(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    liked_only: Annotated[bool | None, Query( description='for see only the liked posts by the user')] = None,
    owns_only: Annotated[bool | None, Query(description='for see only the post created by the user')] = None
    
):
    base_query = db.query(Post)
    if liked_only:
        base_query = base_query.join(Like).filter(Like.user_id == current_user.id)
    if owns_only:
        base_query = base_query.filter(Post.user_id == current_user.id)
        
    return base_query.all()


#====================================================#
#============  Get a Post by ID                               
#====================================================#
@router.get('/{post_id}', response_model=PostFullData, status_code=status.HTTP_200_OK)
def get_detail_post_by_id(
    db: Annotated[Session, Depends(get_db)],
    post_id: Annotated[int, Path(..., description='ID for get the post')],
    current_user: Annotated[User, Depends(get_current_user)],
):
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with ID <{post_id}> not exist.'
        )
            
    return post


#====================================================#
#============  Create a Post                              
#====================================================#
@router.post('/', response_model=PostFullData, status_code=status.HTTP_201_CREATED)
def create_post(
    db: Annotated[Session, Depends(get_db)],
    user_input: Annotated[PostFormFront, Body(..., description='inputs for create a post.')],
    current_user: Annotated[User, Depends(get_current_user)],
):
    existing_post = db.query(Post).filter(Post.title == user_input.title).first()
    if existing_post:
        logger.warning(
            logger_messages.TITLE_ALREADY_EXIST,
            extra={
                'user_id': current_user.id,
                'existing_title': user_input.title,
                'existing_post_id': existing_post.id
                }
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Title <{user_input.title}> already exist.',    
        )
                 
    new_post = Post(**user_input.model_dump())
    new_post.user_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    logger.info(
        logger_messages.NEW_POST_CREATED,
        extra={
            'user_id': current_user.id,
            'new_post_id': new_post.id
        }
    )
    
    return new_post


#====================================================#
#============  Delete a Post by ID                              
#====================================================#
@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task_by_id(
    db: Annotated[Session, Depends(get_db)],
    post_id: Annotated[int, Path(..., description='ID for get the post')],
    current_user: Annotated[User, Depends(get_current_user)],
):
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if post is None:
        logger.warning(
            logger_messages.DELETE_INEXISTANT_POST,
            extra={
                'user_id': current_user.id,
                'post_id_inexistant': post_id
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with ID <{post_id}> not exist.'
        )
    if post.user_id != current_user.id:
        logger.warning(
            logger_messages.DELETE_NOT_OWNER,
            extra={
                'user_id': current_user.id,
                'post_id': post.id
            }
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'this is not your post you can`t modify it.')
        
    db.delete(post)
    db.commit()
    logger.info(
        logger_messages.DELETE_POST_SUCCESS,
        extra={
            'user_id': current_user.id,
            'deleted_post_id': post_id
        }
    )
    
    
#====================================================#
#============  Update a Post by ID                              
#====================================================#
@router.put('/{post_id}', response_model=PostFullData, status_code=status.HTTP_201_CREATED)
def update_post_by_id(
    db: Annotated[Session, Depends(get_db)],
    post_id: Annotated[int, Path(..., description='ID for get the post')],
    user_input: Annotated[PostUpdateFront, Body(..., description='inputs for updated post (not required).')],
    current_user: Annotated[User, Depends(get_current_user)],
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        logger.warning(
            logger_messages.UPDATE_INEXISTANT_POST,
            extra={
                'user_id': current_user.id,
                'inexisting_post_id': post_id
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with ID <{post_id}> not exist.'
        )
        
    if post.user_id != current_user.id:
        logger.warning(
            logger_messages.UPDATE_NOT_OWNER,
            extra={
                'user_id': current_user.id,
                'post_id': post.id,
                'owner_post_id': post.user_id
            }
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'this is not your post you can`t modify it.')
    
    for field, value in user_input.model_dump(exclude_unset=True).items():
        setattr(post, field, value)
        
    db.commit()
    db.refresh(post)
    logger.info(
        logger_messages.UPDATE_POST_SUCCESS,
        extra={
            'user_id': current_user.id,
            'post_id': post.id,
        }
    )
    return post