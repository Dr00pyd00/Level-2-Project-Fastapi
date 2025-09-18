from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.settings import my_settings


engine =create_engine(url=my_settings.DATA_BASE_URL)


SessionLocal = sessionmaker(
                            bind=engine,
                            autoflush=False,
                            autocommit=False
                            )


Base = declarative_base()
""" Parent class for include table in database.
"""


#==== Dependecie ====#
def get_db():
    """
    Generator for get access to the database.

    Yields:
        Session: the database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
#==== Func for init database with new tables ====#
def init_database():
    import app.models
    Base.metadata.create_all(engine)