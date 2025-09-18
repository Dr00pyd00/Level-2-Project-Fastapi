from fastapi import FastAPI
from app.core.database import init_database
from app.routers.posts import router as posts_router
from app.routers.users import router as users_router
from app.routers.likes import router as likes_router


app = FastAPI()

#==== initialize tables in db
# init_database()




#==== Link the router ====#
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(likes_router)