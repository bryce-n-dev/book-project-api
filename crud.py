from sqlalchemy.orm import Session
from sqlalchemy import func

import models, schemas


# Create new user
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(user_id=user.user_id, name=user.name) # Create user with ORM
    db.add(db_user) # Add user to DB
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user information
def get_user(db: Session, user_id: str):
    return (db.query(models.User)
        .filter(models.User.user_id == user_id) # Filter using user_id
        .first())

# Get favourite books
# Join with proper tables to get each book's metadata
# Filter by is_favourite and user_id
def get_favourites(db: Session, user_id: str):
    return (db.query(models.UserBook, models.BookInfo, models.Author.name, models.Genre.genre)
        .join(models.BookInfo, models.UserBook.isbn == models.BookInfo.isbn)
        .join(models.Author, models.BookInfo.author_id == models.Author.author_id)
        .join(models.Genre, models.BookInfo.genre_id == models.Genre.genre_id)
        .filter(models.UserBook.user_id == user_id)
        .filter(models.UserBook.is_favourite == True)
        .all())

# ---Get recommended books---
# Our recommendation system works by analysing the user's friends favourite books.
# Books that are commonly favourited by friends are recommended to the user.
# First we query for the user's current favourite books.
# Then, we query for all books, and count their number of favourites from ALL users/friends.
# Finally, we filter out books that the user already has, in order to not recommend them any books they already know of.
def get_recommended(db: Session, user_id: str):
    user_favourites = (db.query(models.UserBook.isbn)
        .filter(models.UserBook.user_id == user_id)
        .subquery())
    favourite_counts = (db.query(models.UserBook.isbn, func.count(models.UserBook.is_favourite.label('count')))
        .filter(models.UserBook.is_favourite == True)
        .filter(models.UserBook.isbn.not_in(user_favourites))
        .group_by(models.UserBook.isbn).subquery())

    return (db.query(favourite_counts, models.BookInfo, models.Author.name, models.Genre.genre)
        .join(models.BookInfo, favourite_counts.c.isbn == models.BookInfo.isbn)
        .join(models.Author, models.BookInfo.author_id == models.Author.author_id)
        .join(models.Genre, models.BookInfo.genre_id == models.Genre.genre_id)
        .order_by(favourite_counts.c.count.desc())
        .all())

# Get books from database that start with {search} value
def get_books(db: Session, search: str):
    return (db.query(models.BookInfo)
        .filter(models.BookInfo.title
        .contains(search))
        .all())

# Get book by ISBN
def get_book_by_isbn(db: Session, isbn: str):
    return (db.query(models.BookInfo)
        .filter(models.BookInfo.isbn == isbn)
        .first())

# Get user shelf by ID
# Use joins to gather all necessary metadata
def get_user_shelf(db: Session, user_id: str, shelf_id: int):
    return (db.query(models.UserBook, models.BookInfo, models.Author.name, models.Genre.genre)
        .join(models.BookInfo, models.UserBook.isbn == models.BookInfo.isbn)
        .join(models.Author, models.BookInfo.author_id == models.Author.author_id)
        .join(models.Genre, models.BookInfo.genre_id == models.Genre.genre_id)
        .filter(models.UserBook.user_id == user_id)
        .filter(models.UserBook.shelf_id == shelf_id)
        .all())

# Get user book by ISBN
# Use joins to gather all necessary metadata
def get_user_book(db: Session, user_id: str, isbn: str):
    return (db.query(models.UserBook.isbn,models.UserBook.rating, models.UserBook.rating, models.UserBook.is_favourite, models.UserBook.review,models.BookInfo.title, models.BookInfo.cover_url, models.BookInfo.blurb, models.BookInfo.year,models.Author.name, models.Genre.genre)
        .join(models.BookInfo, models.UserBook.isbn == models.BookInfo.isbn)
        .join(models.Author, models.BookInfo.author_id == models.Author.author_id)
        .join(models.Genre, models.Genre.genre_id == models.BookInfo.genre_id)
        .filter(models.UserBook.user_id == user_id)
        .filter(models.UserBook.isbn == isbn)
        .first())

# Can be used to update favourite or update shelf ID
def update_user_book(db: Session, user_id: str, isbn: str, user_book: schemas.UserBookUpdate):
    # First we check to ensure that the user book we want to update actually exists.
    db_user_book = (db.query(models.UserBook)
        .filter(models.UserBook.user_id == user_id)
        .filter(models.UserBook.isbn == isbn)
        .first())

    if db_user_book is not None:
        # Is the input contains an updated is_favourite value, override the previous value.
        if user_book.is_favourite is not None:
            db_user_book.is_favourite = user_book.is_favourite
        # Is the input contains an updated shelf_id value, override the previous value.
        if user_book.shelf_id is not None:
            db_user_book.shelf_id = user_book.shelf_id

    # Add the DB model object to the database.
    db.add(db_user_book)
    db.commit()
    db.refresh(db_user_book)
    return db_user_book

# Delete user book - removes user book from all shelves as a result.
def delete_user_book(db: Session, user_id: str, isbn: str):
    user_book = (db.query(models.UserBook)
        .filter(models.UserBook.user_id == user_id)
        .filter(models.UserBook.isbn == isbn)
        .first())
    db.delete(user_book)
    db.commit()
    return {"Success": True}

# Add book to bookshelf (add entry to DB - user_book)
def create_user_book(db: Session, user_book: schemas.UserBookCreate, user_id: str):
    # Create a new user book
    db_user_book = models.UserBook(isbn=user_book.isbn, user_id=user_id, shelf_id=user_book.shelf_id)

    # Push to database
    db.add(db_user_book)
    db.commit()
    db.refresh(db_user_book)
    return db_user_book