from fastapi import FastAPI

app = FastAPI()


@app.get("/users")
async def get_user(page: int = 1, size: int = 10):
    return {"page": page, "size": size}
