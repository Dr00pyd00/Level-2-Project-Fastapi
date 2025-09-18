
from app.core.database import Base
from app.utils.my_mixins import TimeStampMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property


class Post(TimeStampMixin, Base):
    """
    Class for Post object
   
    Fields:
    - id (int) : autoincrement primary key.
    - title (str) : title of the post.
    - content (str) : content of the post.
    
    


    """
    
    __tablename__ = 'posts'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    
    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )
    
    content: Mapped[str] = mapped_column(
        String(1000),
        nullable=True
    )
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        nullable=False
    )
    
    user = relationship('User', back_populates='posts')
    likes = relationship('Like', back_populates='post', cascade="all, delete-orphan")
    
    @hybrid_property
    def likes_count(self):
        return len(self.likes)