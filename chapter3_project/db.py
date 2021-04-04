from typing import Dict

from chapter3_project.models.user import User
from chapter3_project.models.post import Post


class DummyDatabase:
    users: Dict[int, User] = {}
    posts: Dict[int, Post] = {}


db = DummyDatabase()
