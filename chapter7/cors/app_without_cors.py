from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def get():
    return {"detail": "GET response"}


@app.post("/")
async def post(request: Request):
    json = await request.json()
    return {"detail": "POST response", "input_payload": json}
