import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

from app.database.database_manager import DatabaseManager
from app.utils.paths import DATABASE_PATH


class SessionExportService:
    """
    Exports completed recording session to .session.zip file.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    def export_session(
        self,
        session_id: int,
        output_path: str,
    ) -> None:
        """
        Exports session database, metadata and debug images.
        """

        output_file = Path(output_path)

        temp_dir = output_file.parent / f"_session_{session_id}_export_tmp"

        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        temp_dir.mkdir(parents=True)

        session_db_path = temp_dir / "session.db"
        metadata_path = temp_dir / "metadata.json"
        debug_output_dir = temp_dir / "debug_images"

        debug_output_dir.mkdir()

        shutil.copy2(DATABASE_PATH, session_db_path)

        metadata = self._build_metadata(session_id)

        metadata_path.write_text(
            json.dumps(
                metadata,
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )

        self._copy_debug_images(
            session_id=session_id,
            debug_output_dir=debug_output_dir,
        )

        with zipfile.ZipFile(
            output_file,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as archive:
            for file_path in temp_dir.rglob("*"):
                archive.write(
                    file_path,
                    file_path.relative_to(temp_dir),
                )

        shutil.rmtree(temp_dir)

    def _build_metadata(self, session_id: int) -> dict:
        """
        Builds session metadata.
        """

        with self.database.connect() as connection:
            session = connection.execute(
                """
                SELECT
                    id,
                    name,
                    started_at,
                    ended_at,
                    status,
                    comment
                FROM sessions
                WHERE id = ?
                """,
                (session_id,),
            ).fetchone()

            readings_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM readings
                WHERE session_id = ?
                """,
                (session_id,),
            ).fetchone()[0]

        return {
            "format": "industrial_ocr_session",
            "format_version": 1,
            "exported_at": datetime.now().isoformat(timespec="seconds"),
            "session": dict(session) if session else None,
            "readings_count": readings_count,
        }

    def _copy_debug_images(
        self,
        session_id: int,
        debug_output_dir: Path,
    ) -> None:
        """
        Copies debug images.

        Current implementation copies all debug images.
        Later we can filter them by session if needed.
        """

        debug_source_dir = Path("data/debug")

        if not debug_source_dir.exists():
            return

        for image_path in debug_source_dir.glob("*.png"):
            shutil.copy2(
                image_path,
                debug_output_dir / image_path.name,
            )