# Yeh teen lines sqlalchemy ke tool ko import kar rahi hain
from sqlalchemy import create_engine # create engine : mysql se connection banata hain
from sqlalchemy.ext.declarative import declarative_base # sab ORM models ka base class banata hai
from sqlalchemy.orm import sessionmaker # database ke sath session handle karta hai


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:<password>@localhost:3306/fastapi_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # yeh line actual MySQL connection banata hian
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) #  session creation with local db

Base = declarative_base()
