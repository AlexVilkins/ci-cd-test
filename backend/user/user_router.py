import uuid
from typing import Any

from fastapi import APIRouter, Depends

from user.schemas import ResponseAllUsers, ConstructUser, User, UserResponse

user_data = [
    {"user_id": uuid.uuid4(),
     "name": "Andrey",
     "age": 26,
     "city": "Moscow"},
    {"user_id": uuid.uuid4(),
     "name": "Vasiliy",
     "age": 24,
     "city": None},
    {"user_id": uuid.uuid4(),
     "name": "Alex",
     "age": 21,
     "city": "Spb"},
]


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/all", response_model=list[ResponseAllUsers])
async def get_last_messages():
    res = [ConstructUser(**person) for person in user_data]
    return res

@router.post("/test")
async def get_last_messages(data: User) -> Any:
    d = data.model_dump()
    d["some"] = "ssad"
    return d

