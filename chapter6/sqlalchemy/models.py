from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostDB(PostBase):
    id: int


metadata = sqlalchemy.MetaData()


posts = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("publication_date", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.Text(), nullable=False),
)
