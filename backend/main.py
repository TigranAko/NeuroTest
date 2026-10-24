import logging
from time import perf_counter
from uuid import uuid4

from api.v1.routers import (
    router_answer,
    router_auth,
    router_neurotest,
    router_question,
    router_test,
)
from core.logging_config import configure_logging, request_id_var
from fastapi import FastAPI, Request
from uvicorn import run

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="NeuroTest")
app.include_router(router_auth)
app.include_router(router_neurotest)
app.include_router(router_test)
app.include_router(router_question)
app.include_router(router_answer)


@app.middleware("http")
async def add_request_id(
    request: Request,
    call_next,
):
    request_id = uuid4().hex
    token = request_id_var.set(request_id)
    started_at = perf_counter()
    try:
        logger.info(
            "Запрос начат",
            extra={
                "meta": {
                    "method": request.method,
                    "path": request.url.path,
                },
            },
        )
        response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Запрос завершён с необработанным исключением",
            extra={
                "meta": {
                    "duration_ms": round(duration_ms, 2),
                },
            },
        )
        raise
    else:
        duration_ms = (perf_counter() - started_at) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "Запрос завершён",
            extra={
                "meta": {
                    "duration_ms": round(duration_ms, 2),
                    "status_code": response.status_code,
                },
            },
        )
        return response
    finally:
        request_id_var.reset(token)


if __name__ == "__main__":
    run(app=app, host="0.0.0.0", port=8000)
