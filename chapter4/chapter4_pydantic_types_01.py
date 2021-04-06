from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError


class User(BaseModel):
    email: EmailStr
    website: HttpUrl


# Invalid email
try:
    User(email="jdoe", website="https://www.example.com")
except ValidationError as e:
    print(str(e))
    assert len(e.errors()) == 1


# Invalid URL
try:
    User(email="jdoe@example.com", website="jdoe")
except ValidationError as e:
    print(str(e))
    assert len(e.errors()) == 1


# Valid
user = User(email="jdoe@example.com", website="https://www.example.com")
assert user.email == "jdoe@example.com"
assert user.website.scheme == "https"
assert user.website.host == "www.example.com"
