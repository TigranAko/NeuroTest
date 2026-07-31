from uuid import UUID, uuid4

from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column

from models import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()
