from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/redirect")
async def redirect():
    return RedirectResponse("/new-url")
