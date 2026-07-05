from api.v1.routers.neurotest import router as router_neurotest
from api.v1.routers.question import router as router_question
from api.v1.routers.test import router as router_test
from api.v1.routers.answer import router as router_answer

__all__ = ["router_neurotest", "router_test", "router_question", "router_answer"]
