from uuid import UUID, uuid4

from core.database import Base
from models.question import Question
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Test(Base):
    __tablename__ = "tests"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    questions: Mapped[list["Question"]] = relationship()
