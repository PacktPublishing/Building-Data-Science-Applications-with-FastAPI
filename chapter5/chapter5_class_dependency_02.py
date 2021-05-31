from typing import Tuple

from fastapi import FastAPI, Depends, Query

app = FastAPI()


class Pagination:
    def __init__(self, maximum_limit: int = 100):
        self.maximum_limit = maximum_limit

    async def skip_limit(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=0),
    ) -> Tuple[int, int]:
        capped_limit = min(self.maximum_limit, limit)
        return (skip, capped_limit)

    async def page_size(
        self,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=0),
    ) -> Tuple[int, int]:
        capped_size = min(self.maximum_limit, size)
        return (page, capped_size)


pagination = Pagination(maximum_limit=50)


@app.get("/items")
async def list_items(p: Tuple[int, int] = Depends(pagination.skip_limit)):
    skip, limit = p
    return {"skip": skip, "limit": limit}


@app.get("/things")
async def list_things(p: Tuple[int, int] = Depends(pagination.page_size)):
    page, size = p
    return {"page": page, "size": size}
