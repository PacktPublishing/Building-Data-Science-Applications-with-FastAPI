from datetime import date
from enum import Enum
from typing import List

from pydantic import BaseModel, ValidationError


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"


class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str
    country: str


class Person(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    birthdate: date
    interests: List[str]
    address: Address


# Invalid address
try:
    Person(
        first_name="John",
        last_name="Doe",
        gender=Gender.MALE,
        birthdate="1991-01-01",
        interests=["travel", "sports"],
        address={
            "street_address": "12 Squirell Street",
            "postal_code": "424242",
            "city": "Woodtown",
            # Missing country
        },
    )
except ValidationError as e:
    print(str(e))

# Valid
person = Person(
    first_name="John",
    last_name="Doe",
    gender=Gender.MALE,
    birthdate="1991-01-01",
    interests=["travel", "sports"],
    address={
        "street_address": "12 Squirell Street",
        "postal_code": "424242",
        "city": "Woodtown",
        "country": "US",
    },
)
print(person)
