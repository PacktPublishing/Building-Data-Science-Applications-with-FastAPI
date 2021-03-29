from fastapi import FastAPI, Body

app = FastAPI()


@app.post("/users")
async def create_user(name: str = Body(...), age: int = Body(...)):
    return {"name": name, "age": age}
