from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/license-plates/{license}")
async def get_license_plate(license: str = Path(..., min_length=9, max_length=9)):
    return {"license": license}
