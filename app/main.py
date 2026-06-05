from fastapi import FastAPI

from app.api.product_api import router

app = FastAPI()

app.include_router(router)


