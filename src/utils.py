import datetime
from typing import Union

from database.models import Schedule

import settings


def round_minutes(timestamp: datetime.datetime) -> datetime.datetime:
    timestamp = timestamp.replace(second=0, microsecond=0)
    minute = timestamp.time().minute
    if minute % 15 != 0:
        minute += 15 - (minute % 15)
        if minute == 60:
            timestamp = timestamp.replace(
                hour=timestamp.hour + 1, minute=0
            )
        else:
            timestamp = timestamp.replace(minute=minute)
    return timestamp


def round_to_daytime(timestamp: datetime.datetime) -> datetime.datetime:
    if settings.HOUR_START <= timestamp.hour <= settings.HOUR_END:
        return timestamp
    if 0 <= timestamp.hour <= 8:
        return timestamp.replace(hour=settings.HOUR_START)
    return timestamp.replace(hour=settings.HOUR_START, day=timestamp.day + 1)


def calculate_next_taking(
    timestamp: datetime.datetime, schedule: Schedule
) -> Union[datetime.datetime, int]:
    """
    returns next time for taking medicine if treatment is not over yet
    otherwise returns -1

    Seconds of calculated time are truncated
    """
    timestamp = timestamp.astimezone(tz=datetime.timezone.utc)
    if schedule.end_date is not None and schedule.end_date < timestamp:
        return -1
    if schedule.start_date > timestamp:
        return round_to_daytime(round_minutes(schedule.start_date))
    passed = timestamp - schedule.start_date
    full_rounds = passed / schedule.period
    res = schedule.start_date + schedule.period * (
        int(full_rounds) + 1
    )
    # I think that if next_taking is JUST at the timestamp,
    # animal won't manage to take it anyways - so I go with
    # int(full_rounds) + 1

    return round_to_daytime(round_minutes(res))
