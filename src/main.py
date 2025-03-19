from contextlib import asynccontextmanager
from typing import Annotated

from database.engine import engine
from database.models import Base, Schedule

import pydmodels as pm

from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from fastapi import FastAPI, Depends


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def session_dependency():
    async with session_maker() as session:
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
    return [obj.id]


@app.get("/schedules")
async def return_schedules(
        user_id: int,
        session: SessionDep,
):
    query_res = await session.execute(
        select(Schedule.id).where(Schedule.user_id == user_id)
    )
    return list(query_res.scalars())


@app.get("/schedule")
async def return_schedules(user_id: int, schedule_id: int):
    pass
