from app.database.database_manager import DatabaseManager


class ReadingRepository:
    """
    Repository for OCR reading records.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    def create(
        self,
        roi_id: int,
        value: float | None,
        raw_text: str,
        confidence: float,
    ) -> int:
        """
        Saves OCR reading to database.
        """

        query = """
        INSERT INTO readings (
            roi_id,
            value,
            raw_text,
            confidence
        )
        VALUES (?, ?, ?, ?)
        """

        with self.database.connect() as connection:
            cursor = connection.execute(
                query,
                (
                    roi_id,
                    value,
                    raw_text,
                    confidence,
                ),
            )

            connection.commit()

            return int(cursor.lastrowid)

    def list_by_roi(self, roi_id: int) -> list[dict]:
        """
        Loads readings by ROI id.
        """

        query = """
        SELECT
            id,
            roi_id,
            value,
            raw_text,
            confidence,
            created_at
        FROM readings
        WHERE roi_id = ?
        ORDER BY created_at DESC
        """

        with self.database.connect() as connection:
            rows = connection.execute(query, (roi_id,)).fetchall()

        return [dict(row) for row in rows]