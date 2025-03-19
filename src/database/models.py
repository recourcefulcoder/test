import datetime

from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Schedule(Base):
    __tablename__ = "schedule"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    creation_date: Mapped[datetime.timedelta] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    period: Mapped[datetime.timedelta]
    end_date: Mapped[datetime.timedelta] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user_id: Mapped[int]
