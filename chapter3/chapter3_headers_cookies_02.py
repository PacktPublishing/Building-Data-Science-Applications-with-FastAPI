from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/")
async def header(user_agent: str = Header(...)):
    return {"user_agent": user_agent}
