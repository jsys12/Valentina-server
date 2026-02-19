from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI
from data.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Выполняется при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Выполняется при остановке (опционально)
    await engine.dispose()


app = FastAPI(lifespan=lifespan)



@app.get("/")
@app.get("/index")
def index():
    return FileResponse("../frontend/index.html")