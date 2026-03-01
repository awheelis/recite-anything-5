import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from datetime import date

from app.database import Base
from app.models import User, Plan, Progress, SessionLog
from app.models.plan import PlanStatus
from app.models.session_log import SessionType


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.mark.asyncio
async def test_create_user(db_session):
    user = User(email="test@example.com", password_hash="hashed")
    db_session.add(user)
    await db_session.commit()
    assert user.id is not None
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_create_plan_with_progress(db_session):
    user = User(email="test2@example.com", password_hash="hashed")
    db_session.add(user)
    await db_session.flush()

    plan = Plan(
        user_id=user.id,
        book="Ephesians",
        translation="KJV",
        total_verses=155,
        verses_per_day=1,
        days_per_week=6,
        start_date=date(2026, 3, 1),
        target_date=date(2026, 9, 15),
        status=PlanStatus.active,
    )
    db_session.add(plan)
    await db_session.flush()

    progress = Progress(plan_id=plan.id)
    db_session.add(progress)
    await db_session.commit()

    assert plan.id is not None
    assert progress.current_verse_index == 0
    assert progress.consecutive_retention_days == 0


@pytest.mark.asyncio
async def test_create_session_log(db_session):
    user = User(email="test3@example.com", password_hash="hashed")
    db_session.add(user)
    await db_session.flush()

    plan = Plan(
        user_id=user.id, book="Ephesians", translation="KJV",
        total_verses=155, verses_per_day=1, days_per_week=6,
        start_date=date(2026, 3, 1), target_date=date(2026, 9, 15),
    )
    db_session.add(plan)
    await db_session.flush()

    log = SessionLog(
        plan_id=plan.id,
        date=date(2026, 3, 1),
        session_type=SessionType.daily,
        phases_completed=["yesterdays_verse", "old_verses", "new_verse"],
    )
    db_session.add(log)
    await db_session.commit()

    assert log.id is not None
    assert log.session_type == SessionType.daily
    assert len(log.phases_completed) == 3
