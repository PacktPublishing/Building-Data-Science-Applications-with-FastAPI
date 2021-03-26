from enum import Enum
from fastapi import FastAPI


class UserType(str, Enum):
    STANDARD = "standard"
    ADMIN = "admin"


app = FastAPI()


@app.get("/users/{type}/{id}/")
async def get_user(type: UserType, id: int):
    return {"type": type, "id": id}
