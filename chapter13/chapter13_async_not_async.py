import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/fast")
async def fast():
    return {"endpoint": "fast"}


@app.get("/slow-async")
async def slow_async():
    """Runs in the main process"""
    time.sleep(10)  # Blocking sync operation
    return {"endpoint": "slow-async"}


@app.get("/slow-sync")
def slow_sync():
    """Runs in a thread"""
    time.sleep(10)  # Blocking sync operation
    return {"endpoint": "slow-sync"}
