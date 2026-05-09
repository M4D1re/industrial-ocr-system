from app.database.database_manager import DatabaseManager


class SessionRepository:
    """
    Repository for recording sessions.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    def create(self, name: str) -> int:
        """
        Starts new recording session.
        """

        query = """
        INSERT INTO sessions (
            name,
            status
        )
        VALUES (?, ?)
        """

        with self.database.connect() as connection:
            cursor = connection.execute(
                query,
                (
                    name,
                    "active",
                ),
            )

            connection.commit()

            return int(cursor.lastrowid)

    def finish(self, session_id: int) -> None:
        """
        Finishes recording session.
        """

        query = """
        UPDATE sessions
        SET
            ended_at = CURRENT_TIMESTAMP,
            status = 'completed'
        WHERE id = ?
        """

        with self.database.connect() as connection:
            connection.execute(query, (session_id,))
            connection.commit()

    def get_active_session(self) -> dict | None:
        """
        Returns active session if exists.
        """

        query = """
        SELECT
            id,
            name,
            started_at,
            ended_at,
            status,
            comment
        FROM sessions
        WHERE status = 'active'
        ORDER BY started_at DESC
        LIMIT 1
        """

        with self.database.connect() as connection:
            row = connection.execute(query).fetchone()

        if row is None:
            return None

        return dict(row)