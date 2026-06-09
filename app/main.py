from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.api.product_api import router
from app.utils.response import ResponseUtil


app = FastAPI()

app.include_router(router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    message = "Validation error"
    if errors:
        message = errors[0].get("msg", message)
    return ResponseUtil.error(message)

