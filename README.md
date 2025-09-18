#  Level 2 Project – FastAPI Blog API

##  Description
This is a API project build with **FastAPI** et **PostfgreSQL**, you can :
- Register, add user (JWT Authentication)
- Create, Read, Updated and Delete posts
- Likes system
- Main page can filter the post (likeds, owners)
- Use Alembic for updated the database

---

##  Installation

### 1. Cloner le projet
```python
git clone git@github.com:Dr00pyd00/Level-2-Project-Fastapi.git
cd Level-2-Project-Fastapi
```

### 2. Create virtual env:
```python
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# install dependences:
pip install -r requirements.txt

```

### 3.Setup Environnements for variables:
Create .env File in the root and :
```python
DATABASE_URL=postgresql://user:password@localhost:5432/blog_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Start running server:
```python
uvicorn app.main:app --reload
# or use fastapi dev tool:
fastapi dev
```

------------------------------------------------------------

## API url :
(http://127.0.0.1:8000/docs)[http://127.0.0.1:8000/docs]

------------------------------------------------------------

## Technos:
- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL
- JWT Auth
