import json
import logging
from contextvars import ContextVar
from datetime import UTC, datetime

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


class RequestContextFilter(logging.Filter):
    """Добавляет текущий request_id к LogRecord"""

    def filter(self, record: logging.LogRecord) -> logging.LogRecord:
        record.request_id = request_id_var.get()
        return record


class JsonFormatter(logging.Formatter):
    """Сериализует записи стандартного logging в одну JSON-строку."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
            "meta": getattr(record, "meta", {}),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


def configure_logging() -> None:
    """Единая настройка логирования — вызывается один раз при старте приложения"""
    handler = logging.StreamHandler()
    handler.addFilter(RequestContextFilter())
    handler.setFormatter(JsonFormatter())
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    for name in ("uvicorn", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(name)
        for uvicorn_handler in tuple(uvicorn_logger.handlers):
            uvicorn_logger.removeHandler(uvicorn_handler)
        uvicorn_logger.propagate = True
