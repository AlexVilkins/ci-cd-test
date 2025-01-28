import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ConstructUser(BaseModel):
    user_id: uuid.UUID = Field(strict=True)
    name: str = Field(strict=True)
    age: int = Field(strict=True)
    city: str = Field(strict=True)



class ResponseAllUsers(BaseModel):
    user_id: uuid.UUID = Field(strict=True)
    name: str = Field(strict=True)
    age: int = Field(strict=True)
    city: str = Field(None, strict=True)


class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    age: int
    address: int


class UserResponse(BaseModel):
    name: datetime = Field(strict=True)
    age: int
    address: int
    some: str



