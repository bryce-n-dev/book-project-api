from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date

from database import Base


# models.py 
# These classes are used to define the shape of the database.
# This allows us to manipulate the database more easily, using pythonic code with the SQLAlchemy library.
# See crud.py for these classes in use.

class Author(Base):
    __tablename__ = "author"

    author_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)


class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)


class Language(Base):
    __tablename__ = "language"

    language_id = Column(String, primary_key=True)
    language = Column(String, nullable=False)


class Publisher(Base):
    __tablename__ = "publisher"

    publisher_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)


class Genre(Base):
    __tablename__ = "genre"

    genre_id = Column(String, primary_key=True)
    genre = Column(String, nullable=False)


class BookInfo(Base):
    __tablename__ = "book_info"

    isbn = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    blurb = Column(String)
    cover_url = Column(String)
    page_no = Column(Integer)
    series_pos = Column(Integer)
    author_id = Column(String, ForeignKey("author.author_id"), nullable=False)
    publisher_id = Column(String, ForeignKey("publisher.publisher_id"), nullable=False)
    language_id = Column(String, ForeignKey("language.language_id"), nullable=False)
    genre_id = Column(String, ForeignKey("genre.genre_id"), nullable=False) # Added nullable=False


class Shelf(Base):
    __tablename__ = "shelf"

    shelf_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class UserBook(Base):
    __tablename__ = "user_book"

    isbn = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, primary_key=True, nullable=False)
    shelf_id = Column(Integer, ForeignKey("shelf.shelf_id"), nullable=False)
    pages_read = Column(Integer)
    date_started_reading = Column(Date)
    date_finished_reading = Column(Date)
    rating = Column(Integer)
    review = Column(String)
    is_favourite = Column(Boolean, default=False, nullable=False)
