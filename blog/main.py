from fastapi import FastAPI , Depends
from sqlalchemy.orm import Session
from . import models , schemas , crud
from .database import engine , SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.get("/users", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/users" , response_model = schemas.UserResponse )
def create_user(user: schemas.UserCreate , db:Session = Depends(get_db)):
    return crud.create_user(db=db,user=user)         
