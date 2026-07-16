from contextlib import asynccontextmanager

from api.v1.routers import (
    router_answer,
    router_auth,
    router_neurotest,
    router_question,
    router_test,
)
from core.database import Base, engine
from fastapi import FastAPI
from models.user import User
from uvicorn import run


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        print(User, "Добавляется таблица")
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="NeuroTest", lifespan=lifespan)
app.include_router(router_auth)
app.include_router(router_neurotest)
app.include_router(router_test)
app.include_router(router_question)
app.include_router(router_answer)

if __name__ == "__main__":
    run(app=app, host="0.0.0.0", port=8000)
