from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{type}/{id}/")
async def get_user(type: str, id: int):
    return {"type": type, "id": id}
