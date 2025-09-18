from app.core.database import Base
from app.utils.my_mixins import TimeStampMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer


class User(TimeStampMixin, Base):
    """
    Class for User object
   
    Fields:
    - id (int) : autoincrement primary key.
    - username (str) : username of user => credential.
    - password (str) : password for login etc.
    """
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    
    username: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )
    
    password: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )
    
    posts = relationship('Post', back_populates='user')
    likes = relationship('Like', back_populates='user', cascade='all, delete-orphan')