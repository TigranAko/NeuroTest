from enum import unique
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from core.database import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import Question


class Answer(Base):
    __tablename__ = "answers"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    question_id: Mapped[UUID] = mapped_column(ForeignKey("questions.id"))
    text: Mapped[str] = mapped_column()
    isCorrect: Mapped[bool] = mapped_column(default=False)
    position: Mapped[int] = mapped_column()

    question: Mapped["Question"] = relationship(back_populates="answers")
    __table_args__ = (
        UniqueConstraint("question_id", "position", name="uq_answer_position"),
    )
