from pydantic import BaseModel
from typing import Union


# These classes are used to define what shape of data the API accepts.
# Specifically, in main, we use these classes to define the types of data that each of our endpoints can and cannot accept.

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

# Base class
class UserBookBase(BaseModel):
    pass

# Used for create operations
class UserBookCreate(UserBookBase):
    isbn: str
    shelf_id: int

# Used for update operations
class UserBookUpdate(UserBookBase):
    is_favourite: Union[bool, None] = None
    shelf_id: Union[int, None] = None

# Used for read operations
class UserBook(UserBookBase):
    class Config:
        orm_mode = True