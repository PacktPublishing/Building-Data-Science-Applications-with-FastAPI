from typing import Optional

from fastapi import APIRouter, FastAPI, Depends, Header, HTTPException, status


def secret_header(secret_header: Optional[str] = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":
        raise HTTPException(status.HTTP_403_FORBIDDEN)


router = APIRouter()


@router.get("/route1")
async def router_route1():
    return {"route": "route1"}


@router.get("/route2")
async def router_route2():
    return {"route": "route2"}


app = FastAPI()
app.include_router(router, prefix="/router", dependencies=[Depends(secret_header)])
