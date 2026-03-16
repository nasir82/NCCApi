from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:NtzzBAYQSXrEAJRwLuKYxRtwkYbXKXSx@interchange.proxy.rlwy.net:49581/railway'
# using create engine method creating an engine object to handle the database connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# creating a session local class to handle the database sessions
SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind=engine)
# this is initializing all the tables in the database according to the models defined in the models.py file
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()