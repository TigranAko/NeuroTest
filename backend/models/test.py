from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from models.question import Question


class Test(Base):
    __tablename__ = "tests"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    questions: Mapped[list["Question"]] = relationship(back_populates="test")
