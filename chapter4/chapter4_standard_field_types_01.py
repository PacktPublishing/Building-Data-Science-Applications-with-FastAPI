from pydantic import BaseModel


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int


person = Person(first_name="John", last_name="Doe", age=30)
print(person)  # first_name='John' last_name='Doe' age=30
