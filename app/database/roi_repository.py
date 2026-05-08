from app.database.database_manager import DatabaseManager
from app.models.roi_model import ROIModel


class ROIRepository:
    """
    Repository for ROI database operations.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    def create(self, camera_id: int, roi: ROIModel) -> int:
        """
        Saves ROI to database and returns database id.
        """

        query = """
        INSERT INTO roi_regions (
            camera_id,
            name,
            x,
            y,
            width,
            height,
            enabled,
            polling_interval_sec
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        with self.database.connect() as connection:
            cursor = connection.execute(
                query,
                (
                    camera_id,
                    roi.name,
                    roi.x,
                    roi.y,
                    roi.width,
                    roi.height,
                    int(roi.enabled),
                    roi.polling_interval_sec,
                ),
            )

            connection.commit()

            return int(cursor.lastrowid)

    def delete(self, roi_id: int) -> None:
        """
        Deletes ROI from database.
        """

        with self.database.connect() as connection:
            connection.execute(
                "DELETE FROM roi_regions WHERE id = ?",
                (roi_id,),
            )

            connection.commit()

    def list_by_camera(self, camera_id: int) -> list[ROIModel]:
        """
        Loads ROI regions by camera id.
        """

        query = """
        SELECT
            id,
            name,
            x,
            y,
            width,
            height,
            enabled,
            polling_interval_sec
        FROM roi_regions
        WHERE camera_id = ?
        ORDER BY id
        """

        with self.database.connect() as connection:
            rows = connection.execute(query, (camera_id,)).fetchall()

        return [
            ROIModel(
                id=row["id"],
                name=row["name"],
                x=row["x"],
                y=row["y"],
                width=row["width"],
                height=row["height"],
                enabled=bool(row["enabled"]),
                polling_interval_sec=row["polling_interval_sec"],
            )
            for row in rows
        ]