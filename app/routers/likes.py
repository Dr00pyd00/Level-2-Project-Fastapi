from fastapi import APIRouter, status, Depends, Body, HTTPException, Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.posts import PostFullData, PostFormFront, PostUpdateFront
from app.models.post import Post
from app.models.like import Like
from typing import Annotated
from app.core.security import get_current_user
from app.models.user import User


router = APIRouter(
    prefix='/likes',
    tags=['Likes']
)


@router.post('/{post_id}')
async def toggle_like(
    post_id:int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post ID:{post_id}'
        )
    
    existing_like = db.query(Like).filter(Like.user_id == current_user.id, Like.post_id == post_id).first()
    if existing_like:
        db.delete(existing_like)
        db.commit()
        return {"message": f"User {current_user.username} unliked post {post_id}"}
    
    new_like:Like = Like(user_id=current_user.id, post_id=post_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return {"message": f"User {current_user.username} liked post {post_id}"}