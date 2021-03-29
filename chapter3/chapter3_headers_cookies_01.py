from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/")
async def header(hello: str = Header(...)):
    return {"hello": hello}
