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
    return db.query(models.UserBook.isbn, models.BookInfo.title, models.BookInfo.cover_url).join(models.BookInfo, models.UserBook.isbn == models.BookInfo.isbn).filter(models.UserBook.user_id == user_id).filter(models.UserBook.is_favourite == True).all()

# Get books from database that start with {search} value
def get_books(db: Session, search: str):
    return db.query(models.BookInfo).filter(models.BookInfo.title.like(search + "%")).all()

# Get shelf
def get_user_shelf(db: Session, user_id: str, shelf_id: int):
    return db.query(models.UserBook).filter(models.UserBook.user_id == user_id).filter(models.UserBook.shelf_id == shelf_id).all()

# Get user book
def get_user_book(db: Session, user_id: str, isbn: str):
    return db.query(models.UserBook.isbn,models.UserBook.rating, models.UserBook.rating, models.UserBook.is_favourite, models.UserBook.review,models.BookInfo.title, models.BookInfo.cover_url, models.BookInfo.blurb, models.BookInfo.year,models.Author.name, models.Genre.genre).join(models.BookInfo, models.UserBook.isbn == models.BookInfo.isbn).join(models.Author, models.BookInfo.author_id == models.Author.author_id).join(models.Genre, models.Genre.genre_id == models.BookInfo.genre_id).filter(models.UserBook.user_id == user_id).filter(models.UserBook.isbn == isbn).first()

# Can be used to update favourite or update shelf ID
def update_book(db: Session, user_id: str, isbn: Union[int, None] = None, favourite: Union[bool, None] = None):
    pass

# Remove book from bookshelf (delete entry from DB - user_book)
def delete_book_from_shelf(db: Session, user_id: str, isbn: str):
    pass

# Add book to bookshelf (add entry to DB - user_book)
def add_book_to_shelf(db: Session, book: schemas.Book, user_id: int, isbn: str):
    pass