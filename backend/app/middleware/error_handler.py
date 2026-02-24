from fastapi.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response | JSONResponse:
        try:
            response = await call_next(request)
            return response

        except HTTPException:
            raise

        except Exception as e:
            return JSONResponse(
                {"message": "Ошибка. попробуйте позже."}, status_code=500
            )
