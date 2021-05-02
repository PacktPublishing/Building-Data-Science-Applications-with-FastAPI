from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from tortoise.models import Model
from tortoise import fields


class CommentBase(BaseModel):
    post_id: int
    publication_date: datetime = Field(default_factory=datetime.now)
    content: str

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    pass


class CommentDB(CommentBase):
    id: int


class PostBase(BaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostDB(PostBase):
    id: int


class PostPublic(PostDB):
    comments: List[CommentDB]

    @validator("comments", pre=True)
    def fetch_comments(cls, v):
        return list(v)


class CommentTortoise(Model):
    id = fields.IntField(pk=True, generated=True)
    post = fields.ForeignKeyField(
        "models.PostTortoise", related_name="comments", null=False
    )
    publication_date = fields.DatetimeField(null=False)
    content = fields.TextField(null=False)

    class Meta:
        table = "comments"


class PostTortoise(Model):
    id = fields.IntField(pk=True, generated=True)
    publication_date = fields.DatetimeField(null=False)
    title = fields.CharField(max_length=255, null=False)
    content = fields.TextField(null=False)

    class Meta:
        table = "posts"
