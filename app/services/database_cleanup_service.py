from app.database.database_manager import DatabaseManager


class DatabaseCleanupService:
    """
    Service for safe database cleanup operations.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    def clear_session_data(self) -> None:
        """
        Removes session runtime data but keeps cameras and ROI.
        """

        with self.database.connect() as connection:
            connection.execute("DELETE FROM readings")
            connection.execute("DELETE FROM events")
            connection.execute("DELETE FROM sessions")

            connection.commit()

    def factory_reset(self) -> None:
        """
        Removes all user data and resets SQLite autoincrement counters.
        """

        with self.database.connect() as connection:
            connection.execute("DELETE FROM readings")
            connection.execute("DELETE FROM events")
            connection.execute("DELETE FROM sessions")
            connection.execute("DELETE FROM roi_regions")
            connection.execute("DELETE FROM cameras")

            connection.execute("DELETE FROM sqlite_sequence")

            connection.commit()