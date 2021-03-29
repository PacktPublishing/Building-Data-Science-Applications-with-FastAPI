from typing import Optional

from fastapi import FastAPI, Cookie

app = FastAPI()


@app.get("/")
async def cookie(hello: Optional[str] = Cookie(None)):
    return {"hello": hello}
