from pathlib import Path

from app.database.database_manager import DatabaseManager


def test_database_initialization(tmp_path: Path):
    database_path = tmp_path / "test_app.db"

    database = DatabaseManager(database_path)
    database.initialize()

    with database.connect() as connection:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    table_names = {row["name"] for row in tables}

    assert "cameras" in table_names
    assert "roi_regions" in table_names
    assert "sessions" in table_names
    assert "readings" in table_names
    assert "settings" in table_names