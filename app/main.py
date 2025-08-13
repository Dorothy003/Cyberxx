from fastapi import FastAPI
from .routes import router
from .database import engine, Base
import asyncio

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
