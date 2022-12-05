from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# STANDARD BOILERPLATE WHEN USING SQLALCHEMY
# For more details, check out the documentation: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-parts

# Connect to SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./book_project.db"

# Create engine and local session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()