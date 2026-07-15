from sqlalchemy import text
from app.db.connection import engine


def test_database_connection():
    print("1. About to connect")

    with engine.connect() as conn:
        print("2. Connected")

        result = conn.execute(text("SELECT 1"))

        print("3. Query executed")

        assert result.scalar() == 1

        print("4. Test passed")