import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
import uvicorn

from backend.app.api.v1 import event
from backend.app.core.exceptions_handlers import (
    not_found,
    rate_limit,
    validation_exception_handler,
)
from backend.app.middleware.cors import setup_cors
from backend.app.middleware.error_handler import ExceptionMiddleware
from backend.app.middleware.logger_handler import AccessLogMiddleware
from backend.app.middleware.rollback_handler import (
    SQLAlchemySessionMiddleware,
)
from backend.app.models.session import DBBaseModel, engine
from backend.app.models import models

DBBaseModel.metadata.create_all(bind=engine)

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(status.HTTP_429_TOO_MANY_REQUESTS, rate_limit)
app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found)


setup_cors(app)
app.add_middleware(SQLAlchemySessionMiddleware)
app.add_middleware(ExceptionMiddleware)
app.add_middleware(AccessLogMiddleware)




app.include_router(
    event.router,
    prefix="/api/v1/events",
    tags=["Ручки для управления мероприятиями"],
)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)

# python -m venv venv
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# venv\Scripts\activate || venv\Scripts\activate.bat
# uvicorn backend.app.main:app --host 192.168.0.108 --port 8000 --reload
# ipconfig
# net stop hns; net start hns

# tasklist | findstr uvicorn
# taskkill /PID 12476 /F
