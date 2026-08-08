from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import TimestampMixin

if TYPE_CHECKING:
    from models import Test


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()
    tests: Mapped[list["Test"]] = relationship(back_populates="author")
