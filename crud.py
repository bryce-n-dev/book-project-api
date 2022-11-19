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

# Get favourite books
def get_favourites(db: Session, user_id: str):
    return db.query(models.UserBook.isbn, models.BookInfo.title, models.BookInfo.cover_url).join(models.BookInfo, models.UserBook.isbn == models.BookInfo.isbn).filter(models.UserBook.user_id == user_id).filter(models.UserBook.is_favourite == True).all()

# Get books from database that start with {search} value
def get_books(db: Session, search: str):
    return db.query(models.BookInfo).filter(models.BookInfo.title.contains(search)).all()

def get_book_by_isbn(db: Session, isbn: str):
    return db.query(models.BookInfo).filter(models.BookInfo.isbn == isbn).first()

# Get shelf
def get_user_shelf(db: Session, user_id: str, shelf_id: int):
    return db.query(models.UserBook.isbn, models.BookInfo.title, models.BookInfo.cover_url).join(models.BookInfo, models.UserBook.isbn == models.BookInfo.isbn).filter(models.UserBook.user_id == user_id).filter(models.UserBook.shelf_id == shelf_id).all()

# Get user book
def get_user_book(db: Session, user_id: str, isbn: str):
    return db.query(models.UserBook.isbn,models.UserBook.rating, models.UserBook.rating, models.UserBook.is_favourite, models.UserBook.review,models.BookInfo.title, models.BookInfo.cover_url, models.BookInfo.blurb, models.BookInfo.year,models.Author.name, models.Genre.genre).join(models.BookInfo, models.UserBook.isbn == models.BookInfo.isbn).join(models.Author, models.BookInfo.author_id == models.Author.author_id).join(models.Genre, models.Genre.genre_id == models.BookInfo.genre_id).filter(models.UserBook.user_id == user_id).filter(models.UserBook.isbn == isbn).first()

# Can be used to update favourite or update shelf ID
def update_user_book(db: Session, user_id: str, isbn: Union[int, None] = None, favourite: Union[bool, None] = None):
    pass

# Remove book from bookshelf (delete entry from DB - user_book)
def delete_user_book(db: Session, user_id: str, isbn: str):
    pass

# Add book to bookshelf (add entry to DB - user_book)
def create_user_book(db: Session, user_book: schemas.UserBookCreate, user_id: str):
    db_user_book = models.UserBook(isbn=user_book.isbn, user_id=user_id, shelf_id=user_book.shelf_id)
    db.add(db_user_book)
    db.commit()
    db.refresh(db_user_book)
    return db_user_book