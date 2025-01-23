from pydantic import BaseModel


class ConstructURL(BaseModel):
    url: str


class ResponseAddUrl(BaseModel):
    img_url: str
    position: str
    description: str
    user_id: str





