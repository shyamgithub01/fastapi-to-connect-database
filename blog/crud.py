from sqlalchemy.orm import Session 
from . import models, schemas
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"] , deprecated="auto")
def delete_user_by_name(db: Session, name: str):
    user = db.query(models.User).filter(models.User.name == name).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def get_password_hash(password:str):
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email , password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()