from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from sqlalchemy import text

from .deps import get_db
from .schema import Base


async def lifespan(app: FastAPI):
    if os.getenv("MODE", "producrion") == "development":
        db = await get_db()
        async with db.get_async_engine().begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
            await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)


@app.get("/ping")
async def ping() -> str:
    return "PONG"
