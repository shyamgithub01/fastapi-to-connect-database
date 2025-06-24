from fastapi import FastAPI , Depends
from sqlalchemy.orm import Session
from . import models , schemas , crud
from .database import engine , SessionLocal
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from . import auth
from fastapi import HTTPException
from .crud import delete_user_by_name
from .auth import get_current_user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close
@app.delete("/users/{name}")
def delete_user(name: str, db: Session = Depends(get_db)):
    deleted = delete_user_by_name(db, name)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User '{name}' deleted successfully"}        

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/users", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/users" , response_model = schemas.UserResponse )
def create_user(user: schemas.UserCreate , db:Session = Depends(get_db)):
    return crud.create_user(db=db,user=user)         

@app.get("/me")
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }