from fastapi import FastAPI, Request
from starlette.responses import Response

app = FastAPI()


@app.get("/")
async def get(response: Response):
    response.set_cookie("hello", "world")
    return {"detail": "GET response"}


@app.post("/")
async def post(request: Request):
    json = await request.json()
    return {"detail": "POST response", "input_payload": json}
