import datetime
from typing import Union

from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Schedule(Base):
    __tablename__ = "schedule"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    start_date: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow()
    )
    period: Mapped[datetime.timedelta]
    end_date: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    user_id: Mapped[int]

    def __init__(self, *args, **kwargs):
        duration = None
        if "duration" in kwargs.keys():
            duration = kwargs["duration"]
            del kwargs["duration"]
        super().__init__(**kwargs)
        if self.start_date is None:
            self.start_date = datetime.datetime.utcnow()
        if duration is not None:
            self.duration = duration

    @property
    def duration(self) -> Union[int, datetime.timedelta]:
        if self.start_date is None:
            raise ValueError("Creation date not specified!")
        if self.end_date is None:
            return -1
        return self.end_date - self.start_date

    @duration.setter
    def duration(self, value: datetime.timedelta):
        if self.start_date is None:
            raise ValueError("creation date not specified!")
        self.end_date = self.start_date + value

