from pydantic import BaseModel
from typing import Union


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


class UserBookBase(BaseModel):
    pass

class UserBookCreate(UserBookBase):
    isbn: str
    shelf_id: int

class UserBookUpdate(UserBookBase):
    is_favourite: Union[bool, None] = None
    shelf_id: Union[int, None] = None

class UserBook(UserBookBase):
    class Config:
        orm_mode = True