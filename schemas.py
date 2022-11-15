from pydantic import BaseModel


# Base class
class UserBase(BaseModel):
    user_id: str
    name: str

# Used for create operations
class UserCreate(UserBase):
    pass

# Used for read operations
class User(UserBase):
    class Config:
        orm_mode = True


class Book(BaseModel):
    isbn: str