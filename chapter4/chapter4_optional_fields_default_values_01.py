from typing import Optional

from pydantic import BaseModel


class UserProfile(BaseModel):
    nickname: str
    location: Optional[str] = None
    subscribed_newsletter: bool = True


user = UserProfile(nickname="jdoe")
assert user.location is None
assert user.subscribed_newsletter is True
