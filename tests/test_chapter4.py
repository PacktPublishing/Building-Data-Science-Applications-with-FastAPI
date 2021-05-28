from datetime import date
import runpy

import httpx
import pytest
from fastapi import status
from pydantic import ValidationError

from chapter4.chapter4_working_pydantic_objects_04 import (
    app as chapter4_working_pydantic_objects_04_app,
)
from chapter4.chapter4_working_pydantic_objects_05 import (
    app as chapter4_working_pydantic_objects_05_app,
    db,
    PostDB,
)


def test_chapter4_custom_validation_01():
    from chapter4.chapter4_custom_validation_01 import Person

    # Invalid birthdate
    try:
        Person(first_name="John", last_name="Doe", birthdate="1800-01-01")
    except ValidationError as e:
        assert len(e.errors()) == 1

    person = Person(first_name="John", last_name="Doe", birthdate="1991-01-01")
    assert isinstance(person, Person)


def test_chapter4_custom_validation_02():
    from chapter4.chapter4_custom_validation_02 import UserRegistration

    # Passwords not matching
    try:
        UserRegistration(
            email="jdoe@example.com", password="aa", password_confirmation="bb"
        )
    except ValidationError as e:
        assert len(e.errors()) == 1

    # Valid
    user_registration = UserRegistration(
        email="jdoe@example.com", password="aa", password_confirmation="aa"
    )
    assert isinstance(user_registration, UserRegistration)


def test_chapter4_custom_validation_03():
    from chapter4.chapter4_custom_validation_03 import m

    assert m.values == [1, 2, 3]


def test_chapter4_fields_validation_01():
    from chapter4.chapter4_fields_validation_01 import Person

    # Invalid first name
    try:
        Person(first_name="J", last_name="Doe", age=30)
    except ValidationError as e:
        assert len(e.errors()) == 1

    # Invalid age
    try:
        Person(first_name="John", last_name="Doe", age=2000)
    except ValidationError as e:
        assert len(e.errors()) == 1

    # Valid
    person = Person(first_name="John", last_name="Doe", age=30)
    assert person.first_name == "John"
    assert person.last_name == "Doe"
    assert person.age == 30


def test_chapter4_fields_validation_02():
    from chapter4.chapter4_fields_validation_02 import o1, o2

    assert o1.l == ["a", "b", "c", "d"]
    assert o1.l2 == []

    assert o2.l == ["a", "b", "c"]
    assert o1.l2 == []

    assert o1.d < o2.d


def test_chapter4_optional_fields_default_values_01():
    from chapter4.chapter4_optional_fields_default_values_01 import user

    assert user.location is None
    assert user.subscribed_newsletter is True


def test_chapter4_optional_fields_default_values_02():
    from chapter4.chapter4_optional_fields_default_values_02 import o1, o2

    assert o1 == o2


def test_chapter4_pydantic_types_01():
    from chapter4.chapter4_pydantic_types_01 import User

    # Invalid email
    try:
        User(email="jdoe", website="https://www.example.com")
    except ValidationError as e:
        assert len(e.errors()) == 1

    # Invalid URL
    try:
        User(email="jdoe@example.com", website="jdoe")
    except ValidationError as e:
        print(str(e))

    # Valid
    user = User(email="jdoe@example.com", website="https://www.example.com")
    assert user.email == "jdoe@example.com"
    assert user.website.scheme == "https"
    assert user.website.host == "www.example.com"


def test_chapter4_standard_field_types_01():
    from chapter4.chapter4_standard_field_types_01 import Person, person

    assert isinstance(person, Person)


def test_chapter4_standard_field_types_02():
    from chapter4.chapter4_standard_field_types_02 import Gender, Person

    # Invalid gender
    try:
        Person(
            first_name="John",
            last_name="Doe",
            gender="INVALID_VALUE",
            birthdate="1991-01-01",
            interests=["travel", "sports"],
        )
    except ValidationError as e:
        assert len(e.errors()) == 1

    # Invalid birthdate
    try:
        Person(
            first_name="John",
            last_name="Doe",
            gender=Gender.MALE,
            birthdate="1991-13-42",
            interests=["travel", "sports"],
        )
    except ValidationError as e:
        assert len(e.errors()) == 1

    # Valid
    person = Person(
        first_name="John",
        last_name="Doe",
        gender=Gender.MALE,
        birthdate="1991-01-01",
        interests=["travel", "sports"],
    )
    assert person.gender == Gender.MALE
    assert person.birthdate == date(1991, 1, 1)
    assert person.interests == ["travel", "sports"]


def test_chapter4_standard_field_types_03():
    from chapter4.chapter4_standard_field_types_03 import Address, Gender, Person

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
        assert len(e.errors()) == 1

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
    assert isinstance(person.address, Address)


def test_chapter4_working_pydantic_objects_01():
    from chapter4.chapter4_working_pydantic_objects_01 import person_dict

    assert person_dict["first_name"] == "John"
    assert person_dict["address"]["street_address"] == "12 Squirell Street"


def test_chapter4_working_pydantic_objects_02():
    from chapter4.chapter4_working_pydantic_objects_02 import (
        person_include,
        person_exclude,
        person_nested_include,
    )

    assert person_include == {"first_name": "John", "last_name": "Doe"}

    assert "birthdate" not in person_exclude
    assert "interests" not in person_exclude

    assert person_nested_include == {
        "first_name": "John",
        "last_name": "Doe",
        "address": {"city": "Woodtown", "country": "US"},
    }


def test_chapter4_working_pydantic_objects_03():
    from chapter4.chapter4_working_pydantic_objects_03 import name_dict

    assert name_dict == {"first_name": "John", "last_name": "Doe"}


@pytest.mark.fastapi(app=chapter4_working_pydantic_objects_04_app)
@pytest.mark.asyncio
class TestWorkingPydanticObjects04:
    async def test_invalid_payload(self, client: httpx.AsyncClient):
        response = await client.post("/posts", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_payload(self, client: httpx.AsyncClient):
        response = await client.post("/posts", json={"title": "Foo", "content": "Bar"})

        assert response.status_code == status.HTTP_201_CREATED
        json = response.json()
        assert json == {"id": 1, "title": "Foo", "content": "Bar"}


@pytest.mark.fastapi(app=chapter4_working_pydantic_objects_05_app)
@pytest.mark.asyncio
class TestWorkingPydanticObjects05:
    async def test_not_existing_post(self, client: httpx.AsyncClient):
        response = await client.patch("/posts/1", json={})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_valid_payload(self, client: httpx.AsyncClient):
        db.posts = {1: PostDB(id=1, title="Foo", content="Bar")}
        response = await client.patch("/posts/1", json={"title": "New title"})

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"id": 1, "title": "New title", "content": "Bar"}
