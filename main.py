from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

import crud, schemas
from database import SessionLocal


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create new user
@app.post("/users", tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already created")
    return crud.create_user(db, user)

# Get user information
@app.get("/users/{user_id}", tags=["users"])
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Get favourite books
@app.get("/users/{user_id}/favourites", tags=["shelves"])
def get_favourites(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_favourites(db, user_id)

# Get books from database that start with {search} value
@app.get("/books", tags=["public"])
def get_books(search: str, db: Session = Depends(get_db)):
    return crud.get_books(db, search)

# Get shelf
@app.get("/users/{user_id}/shelves/{shelf_id}", tags=["shelves"])
def get_user_shelf(user_id: str, shelf_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_user_shelf(db, user_id, shelf_id)

# Get user book
@app.get("/users/{user_id}/books/{isbn}", tags=["user-books"])
def get_user_book(user_id: str, isbn: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_book = crud.get_user_book(db, user_id, isbn)
    if db_book is None:
        raise HTTPException(status_code=404, detail="User book not found")
    return db_book

# Can be used to update favourite or update shelf ID
@app.put("/users/{user_id}/books/{isbn}", tags=["user-books"])
def update_user_book(user_id: str, isbn: str, user_book: schemas.UserBookUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user_book = crud.get_user_book(db, user_id=user_id, isbn=isbn)
    if db_user_book is None:
        raise HTTPException(status_code=404, detail="User book not found")
    return crud.update_user_book(db, user_id=user_id, isbn=isbn, user_book=user_book)

# Remove book from bookshelf (delete entry from DB - user_book)
@app.delete("/users/{user_id}/books/{isbn}", tags=["user-books"])
def delete_user_book(user_id: str, isbn: str, db: Session = Depends(get_db)):
    user_book = crud.get_user_book(db, user_id=user_id, isbn=isbn)
    if user_book is None:
        raise HTTPException(status_code=404, detail="User book not found")
    return crud.delete_user_book(db, user_id=user_id, isbn=isbn)

# Add book to bookshelf (add entry to DB - user_book)
@app.post("/users/{user_id}/books", tags=["user-books"])
def create_user_book(user_book: schemas.UserBookCreate, user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_book = crud.get_book_by_isbn(db, isbn=user_book.isbn)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book ISBN does not exist")
    db_user_book = crud.get_user_book(db, user_id=user_id, isbn=user_book.isbn)
    if db_user_book is not None:
        raise HTTPException(status_code=400, detail="User book already exists")
    return crud.create_user_book(db, user_book=user_book, user_id=user_id)