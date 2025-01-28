import re

from pydantic import BaseModel, Field, field_validator


class ConstructURL(BaseModel):
    url: str


class ResponseAddUrl(BaseModel):
    img_url: str = Field(strict=True)
    position: int = Field(strict=True)
    description: str = Field(strict=True)
    user_id: str = Field(strict=True)

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value: str) -> str:
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', value):
            raise ValueError("user_id must be in the format '123.12.123.12' with each number 1-3 digits.")
        return value





