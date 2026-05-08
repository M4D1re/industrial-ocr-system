import sqlite3
from pathlib import Path

from app.utils.paths import DATABASE_PATH


class DatabaseManager:
    """
    SQLite database manager.

    Responsible for:
    - opening connections
    - applying migrations
    - providing database access
    """

    def __init__(self, database_path: Path = DATABASE_PATH) -> None:
        self.database_path = database_path

    def connect(self) -> sqlite3.Connection:
        """
        Creates SQLite connection.
        """

        connection = sqlite3.connect(self.database_path)

        connection.row_factory = sqlite3.Row

        connection.execute("PRAGMA foreign_keys = ON;")

        return connection

    def initialize(self) -> None:
        """
        Initializes database schema.
        """

        migration_path = (
            Path(__file__).resolve().parent
            / "migrations"
            / "001_initial_schema.sql"
        )

        sql = migration_path.read_text(encoding="utf-8")

        with self.connect() as connection:
            connection.executescript(sql)
            connection.commit()