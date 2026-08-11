from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from core.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models import Question, User


class Test(Base):
    __tablename__ = "tests"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    questions: Mapped[list["Question"]] = relationship(back_populates="test")
    author: Mapped["User"] = relationship(back_populates="tests")
