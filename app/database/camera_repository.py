from app.database.database_manager import DatabaseManager
from app.models.camera_model import CameraModel


class CameraRepository:
    """
    Repository for camera database operations.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

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

            cursor = connection.execute(
                """
                INSERT INTO cameras (name, source, enabled)
                VALUES (?, ?, ?)
                """,
                ("Default Webcam", "0", 1),
            )

            connection.commit()

            return CameraModel(
                id=int(cursor.lastrowid),
                name="Default Webcam",
                source="0",
                enabled=True,
            )