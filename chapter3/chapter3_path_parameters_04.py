from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/users/{id}")
async def get_user(id: int = Path(..., ge=1)):
    return {"id": id}
