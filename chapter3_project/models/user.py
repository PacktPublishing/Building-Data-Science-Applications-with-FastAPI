from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str


class User(BaseModel):
    id: int
    email: str
