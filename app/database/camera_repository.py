from app.database.database_manager import DatabaseManager
from app.models.camera_model import CameraModel


class CameraRepository:
    """
    Repository for camera database operations.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    def create(
        self,
        name: str,
        source: str,
        enabled: bool = True,
    ) -> CameraModel:
        """
        Creates camera record.
        """

        with self.database.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO cameras (name, source, enabled)
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    source,
                    int(enabled),
                ),
            )

            connection.commit()

            return CameraModel(
                id=int(cursor.lastrowid),
                name=name,
                source=source,
                enabled=enabled,
            )

    def list_all(self) -> list[CameraModel]:
        """
        Loads all cameras.
        """

        with self.database.connect() as connection:
            rows = connection.execute(
                """
                SELECT id, name, source, enabled
                FROM cameras
                ORDER BY id
                """
            ).fetchall()

        return [
            CameraModel(
                id=row["id"],
                name=row["name"],
                source=row["source"],
                enabled=bool(row["enabled"]),
            )
            for row in rows
        ]

    def get_or_create_default_camera(self) -> CameraModel:
        """
        Returns default webcam camera record.

        For now we use source '0' as default USB webcam.
        """

        with self.database.connect() as connection:
            row = connection.execute(
                """
                SELECT id, name, source, enabled
                FROM cameras
                WHERE source = ?
                """,
                ("0",),
            ).fetchone()

            if row:
                return CameraModel(
                    id=row["id"],
                    name=row["name"],
                    source=row["source"],
                    enabled=bool(row["enabled"]),
                )

        return self.create(
            name="Default Webcam",
            source="0",
            enabled=True,
        )