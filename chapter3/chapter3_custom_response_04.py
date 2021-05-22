from os import path

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/cat")
async def get_cat():
    root_directory = path.dirname(path.dirname(__file__))
    picture_path = path.join(root_directory, "assets", "cat.jpg")
    return FileResponse(picture_path)
