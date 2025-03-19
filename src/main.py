from contextlib import asynccontextmanager
import datetime
from typing import Annotated

import settings
from database.engine import engine
from database.models import Base, Schedule

import pydmodels as pm

from sqlalchemy.sql import select, text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from fastapi import FastAPI, Depends, Response, status

from utils import calculate_next_taking


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def session_dependency():
    async with session_maker() as session:
        async with session.begin():
            await session.execute(text("SET TIME ZONE 'UTC';"))
        yield session


SessionDep = Annotated[AsyncSession, Depends(session_dependency)]


app = FastAPI(lifespan=lifespan)


@app.post("/schedule")
async def create_schedule(
        session: SessionDep,
        schedule: pm.ScheduleCreationModel
):
    obj = Schedule(**schedule.model_dump())
    session.add(obj)
    await session.commit()
    return obj.id


@app.get("/schedule")
async def return_schedules(
    user_id: int,
    schedule_id: int,
    session: SessionDep,
    response: Response,
):
    qres = await session.execute(
        select(Schedule).where(Schedule.id == schedule_id)
    )
    schedule = qres.scalar()
    if schedule.user_id != user_id:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"error": "invalid access id"}

    res = schedule.__dict__
    if res["end_date"] is not None:
        res["end_date"] = res["end_date"].astimezone()
    res["start_date"] = res["start_date"].astimezone()
    res["today-takings"] = []

    today = datetime.datetime.now(datetime.timezone.utc)
    prev_taking = calculate_next_taking(today, schedule)
    while prev_taking.day == today.day:
        res["today-takings"].append(prev_taking.astimezone().time())
        prev_taking = calculate_next_taking(prev_taking, schedule)
    return res


@app.get("/schedules")
async def return_schedules(
        user_id: int,
        session: SessionDep,
):
    query_res = await session.execute(
        select(Schedule.id).where(Schedule.user_id == user_id)
    )
    return list(query_res.scalars())


@app.get("/next_takings")
async def evaluate_takings(
        user_id: int,
        session: SessionDep,
):
    qres = await session.execute(
        select(Schedule).where(Schedule.user_id == user_id)
    )
    schedules = qres.scalars()
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    takings = dict()
    for schedule in schedules:
        takings[schedule.name] = []
        prev_taking = timestamp
        while prev_taking <= timestamp + settings.CLOSE_PERIOD:
            next_taking = calculate_next_taking(prev_taking, schedule)
            takings[schedule.name].append(next_taking.time())
            prev_taking = next_taking
    return takings
