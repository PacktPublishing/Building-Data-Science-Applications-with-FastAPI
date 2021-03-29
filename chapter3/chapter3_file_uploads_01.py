from fastapi import FastAPI, File

app = FastAPI()


@app.post("/upload")
async def upload(file: bytes = File(...)):
    return {"file_size": len(file)}
