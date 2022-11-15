from sqlalchemy.orm import Session
from typing import Union

import models, schemas


# Create new user
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(user_id=user.user_id, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user information
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

# Update user information
def update_user(db: Session, user_id: str):
    pass

# Delete user
def delete_user(db: Session, user_id: str):
    pass

# Get favourite books
def get_favourites(db: Session, user_id: str):
    db.query()

# Get {integer} most liked books
def get_top_favourites(db: Session, amount: int = 5):
    db.query()

# Get books from database that start with {search} value
def get_books(db: Session, search: str):
    db.query()

# Get user recommendations
def get_user_recommendations(db: Session, user_id: str):
    pass

# Get shelf
def get_user_shelf(db: Session, user_id: str, shelf_id: int):
    db.query()

# Get user book
def get_user_book(db: Session, user_id: str, isbn: str):
    db.query()

# Can be used to update favourite or update shelf ID
def update_book(db: Session, user_id: str, isbn: Union[int, None] = None, favourite: Union[bool, None] = None):
    pass

# Remove book from bookshelf (delete entry from DB - user_book)
def delete_book_from_shelf(db: Session, user_id: str, isbn: str):
    pass

# Add book to bookshelf (add entry to DB - user_book)
def add_book_to_shelf(db: Session, book: schemas.Book, user_id: int, isbn: str):
    pass