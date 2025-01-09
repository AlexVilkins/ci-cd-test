import uuid
from typing import Optional

from pydantic import BaseModel


class ConstructUser(BaseModel):
    user_id: uuid.UUID
    name: str
    age: int
    city: Optional[str] = None


class ResponseAllUsers(BaseModel):
    user_id: uuid.UUID
    name: str
    age: int
    city: Optional[str] = None





