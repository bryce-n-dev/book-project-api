from sqlalchemy.orm import Session
from typing import Union
from fastapi import Depends, FastAPI, HTTPException

import crud, models, schemas
from database import SessionLocal, engine


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
    db_user = crud.get_user(db, user)
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

# Update user information
@app.put("/users/{user_id}", tags=["users"])
def update_user(user_id: str, db: Session = Depends(get_db)):
    pass

# Delete user
@app.delete("/users/{user_id}", tags=["users"])
def delete_user(user_id: str, db: Session = Depends(get_db)):
    pass

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
def update_book(user_id: str, isbn: Union[int, None] = None, favourite: Union[bool, None] = None, db: Session = Depends(get_db)):
    pass

# Remove book from bookshelf (delete entry from DB - user_book)
@app.delete("/users/{user_id}/books/{isbn}", tags=["user-books"])
def delete_book_from_shelf(user_id: str, isbn: str, db: Session = Depends(get_db)):
    pass

# Add book to bookshelf (add entry to DB - user_book)
@app.post("/users/{user_id}/books/{isbn}", tags=["user-books"])
def add_book_to_shelf(book: schemas.Book, user_id: int, isbn: str, db: Session = Depends(get_db)):
    pass