import re

from pydantic import BaseModel, Field, field_validator
from fastapi import Query


class ConstructURL(BaseModel):
    url: str = Field(strict=True)

    @classmethod
    def as_query(cls, url: str = Query(...,
                                       example="https://youtu.be/fo5KYjqPfWs?si=Y-QgDdIf16BAx5EZ",
                                       description="Ссылка на видео YouTube")):
        return cls(url=url)


class ResponseAddUrl(BaseModel):
    img_url: str = Field(
        strict=True,
        examples=["https://i.ytimg.com/vi/_AggKPqyz6Q/maxresdefault.jpg"],
        description="Cсылка на изображение превью видео",
    )
    position: int = Field(
        strict=True,
        examples=[3],
        description="Позиция в очереди на загрузку (позиция 1 означает что загрузка началась)",
    )
    description: str = Field(
        strict=True,
        examples=["Мое первое видео на YouTube"],
        description="Название видео",
    )
    user_id: str = Field(
        strict=True,
        examples=["172.12.123.4"],
        description="IP адрес отправителя запроса",
    )

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value: str) -> str:
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', value):
            raise ValueError("user_id must be in the format '123.12.123.12' with each number 1-3 digits.")
        return value
