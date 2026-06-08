from fastapi.responses import JSONResponse


class ResponseUtil:

    @staticmethod
    def success(data=None, message="Success", **kwargs):
        response = {
            "status": True,
            "message": message,
            "data": data
        }

        response.update(kwargs)

        return response

    @staticmethod
    def error(message, status_code=400):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": False,
                "message": message
            }
        )
