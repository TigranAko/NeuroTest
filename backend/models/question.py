from uuid import UUID, uuid4

from core.database import Base
from models.answer import Answer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    answers: Mapped[list["Answer"]] = relationship()
