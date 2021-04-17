from typing import Tuple

from fastapi import FastAPI, Depends

app = FastAPI()


async def pagination(skip: int = 0, limit: int = 10) -> Tuple[int, int]:
    return (skip, limit)


@app.get("/items")
async def list_items(p: Tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}


@app.get("/things")
async def list_things(p: Tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}
