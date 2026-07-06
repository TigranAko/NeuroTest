from api.v1.routers.answer import router as router_answer
from api.v1.routers.neurotest import router as router_neurotest
from api.v1.routers.question import router as router_question
from api.v1.routers.test import router as router_test

__all__ = ["router_answer", "router_neurotest", "router_question", "router_test"]
