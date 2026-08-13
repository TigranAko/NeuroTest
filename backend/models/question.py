from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from core.database import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import Answer, Test


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    test_id: Mapped[UUID] = mapped_column(ForeignKey("tests.id"))
    text: Mapped[str] = mapped_column()
    position: Mapped[int] = mapped_column()

    test: Mapped["Test"] = relationship(back_populates="questions")
    answers: Mapped[list["Answer"]] = relationship(back_populates="question")
    __table_args__ = (
        UniqueConstraint("test_id", "position", name="uq_question_position"),
    )
