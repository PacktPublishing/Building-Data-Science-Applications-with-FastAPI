from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


def list_factory():
    return ["a", "b", "c"]


class Model(BaseModel):
    l: List[str] = Field(default_factory=list_factory)
    d: datetime = Field(default_factory=datetime.now)
    l2: List[str] = Field(default_factory=list)


o1 = Model()
assert o1.l == ["a", "b", "c"]
assert o1.l2 == []

o1.l.append("d")
assert o1.l == ["a", "b", "c", "d"]

o2 = Model()
assert o2.l == ["a", "b", "c"]
assert o1.l2 == []

assert o1.d < o2.d
