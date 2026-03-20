from fastapi import FastAPI
from app.api import all_routers

app = FastAPI()


for router in all_routers:
    app.include_router(router)