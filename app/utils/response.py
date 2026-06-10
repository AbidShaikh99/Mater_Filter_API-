from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request


class ResponseUtil:

    def success(data=None, message="Success", **kwargs):
        response = {
            "status": True,
            "message": message,
            "data": data
        }

        response.update(kwargs)

        return response

    
    def error(message, status_code=400):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": False,
                "message": message
            }
        )
# app = FastAPI() 
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     errors = exc.errors()
#     message = "Validation error"
#     if errors:
#         message = errors[0].get("msg", message)
#     return ResponseUtil.error(message)