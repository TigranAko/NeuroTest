from uuid import UUID, uuid4

from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Answer(Base):
    __tablename__ = "answers"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    text: Mapped[str] = mapped_column(unique=True)
    isCorrect: Mapped[bool] = mapped_column(default=False)
