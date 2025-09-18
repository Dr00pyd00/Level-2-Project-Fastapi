from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column, Mapped



class TimeStampMixin():
    """
    Mixin for add fields:
        - created_at (datetime)
        - updated_at (datetime)
    """
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )