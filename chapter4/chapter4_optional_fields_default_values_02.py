from typing import List

from pydantic import BaseModel


class Model(BaseModel):
    # Don't do this.
    # This example shows you why it doesn't work.
    l: List[str] = ["a", "b", "c"]


o1 = Model()
assert o1.l == ["a", "b", "c"]

o1.l.append("d")
assert o1.l == ["a", "b", "c", "d"]

o2 = Model()
print(o2.l)  # ["a", "b", "c", "d"]
