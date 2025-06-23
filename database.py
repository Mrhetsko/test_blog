from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Connect to the Dockerized MySQL database
# User: root
# Password: mysecretpassword
# Host: localhost
# Database: fastapi_task_db
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:mysecretpassword@localhost/fastapi_task_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()