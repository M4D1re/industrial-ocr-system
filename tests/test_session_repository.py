from pathlib import Path

from app.database.database_manager import DatabaseManager
from app.database.session_repository import SessionRepository


def test_create_and_finish_session(tmp_path: Path):
    database_path = tmp_path / "test_app.db"

    database = DatabaseManager(database_path)
    database.initialize()

    repository = SessionRepository(database)

    session_id = repository.create("Test Session")

    active_session = repository.get_active_session()

    assert active_session is not None
    assert active_session["id"] == session_id
    assert active_session["status"] == "active"

    repository.finish(session_id)

    active_session_after_finish = repository.get_active_session()

    assert active_session_after_finish is None