from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from core.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.question import Question


class Answer(Base):
    __tablename__ = "answers"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id"))
    text: Mapped[str] = mapped_column(unique=True)
    isCorrect: Mapped[bool] = mapped_column(default=False)

    question: Mapped["Question"] = relationship(back_populates="answers")
