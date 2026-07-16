from api.v1.routers import (
    router_answer,
    router_auth,
    router_neurotest,
    router_question,
    router_test,
)
from fastapi import FastAPI
from uvicorn import run

app = FastAPI(title="NeuroTest")
app.include_router(router_auth)
app.include_router(router_neurotest)
app.include_router(router_test)
app.include_router(router_question)
app.include_router(router_answer)

if __name__ == "__main__":
    run(app=app, host="0.0.0.0", port=8000)
