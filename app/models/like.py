
from app.core.database import Base
from app.utils.my_mixins import TimeStampMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey





class Like(TimeStampMixin, Base):
    
    __tablename__ = 'likes'
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
        primary_key=True
    )
    
    post_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('posts.id'),
        nullable=False,
        primary_key=True
    )
    
    
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')
    
    def __init__(self, user_id: int, post_id: int):
        self.user_id = user_id
        self.post_id = post_id