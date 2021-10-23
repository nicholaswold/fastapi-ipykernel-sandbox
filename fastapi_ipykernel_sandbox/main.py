import uvicorn
from fastapi import FastAPI

from .routers import routers

app = FastAPI()

for router in routers:
    app.include_router(router)


def start():
    uvicorn.run(
        "fastapi_ipykernel_sandbox.main:app", host="0.0.0.0", port=8000, reload=True
    )
