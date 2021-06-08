from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int


@app.post("/persons", status_code=status.HTTP_201_CREATED)
async def create_person(person: Person):
    return person
