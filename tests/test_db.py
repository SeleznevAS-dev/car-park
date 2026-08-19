import pytest
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from core.config import settings
from core.database import async_session_maker


@pytest.mark.asyncio
async def test_db_connection():
    try:
        async with async_session_maker() as session:
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1
            print(f"✅ Подключение к БД успешно! URL: {settings.DATABASE_URL}")
    except OperationalError as e:
        pytest.fail(f"❌ Не удалось подключиться к БД: {e}")
