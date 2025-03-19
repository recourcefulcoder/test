import datetime
from typing import Optional

from pydantic import BaseModel


class ScheduleCreationModel(BaseModel):
    name: str
    period: datetime.timedelta
    end_date: Optional[datetime.datetime] = None
    user_id: int
