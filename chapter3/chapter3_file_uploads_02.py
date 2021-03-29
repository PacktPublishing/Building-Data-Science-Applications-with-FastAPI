from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"file_name": file.filename, "content_type": file.content_type}
