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

        existing_camera = self.get_by_source(source)

        if existing_camera is not None:
            return existing_camera

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

    def get_by_source(self, source: str) -> CameraModel | None:
        """
        Returns camera by source if it exists.
        """

        with self.database.connect() as connection:
            row = connection.execute(
                """
                SELECT id, name, source, enabled
                FROM cameras
                WHERE source = ?
                """,
                (source,),
            ).fetchone()

        if row is None:
            return None

        return CameraModel(
            id=row["id"],
            name=row["name"],
            source=row["source"],
            enabled=bool(row["enabled"]),
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
        """

        return self.create(
            name="USB Camera 0",
            source="0",
            enabled=False,
        )


    def set_enabled(
            self,
            camera_id: int,
            enabled: bool,
    ) -> None:
        """
        Enables or disables camera.
        """

        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE cameras
                SET enabled = ?
                WHERE id = ?
                """,
                (
                    int(enabled),
                    camera_id,
                ),
            )

            connection.commit()

    def disable_all(self) -> None:
        """
        Disables all cameras.
        Used on application startup to prevent automatic camera activation.
        """

        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE cameras
                SET enabled = 0
                """
            )

            connection.commit()