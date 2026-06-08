# from pathlib import Path
#
# from app.database.camera_repository import CameraRepository
# from app.database.database_manager import DatabaseManager
# from app.database.reading_repository import ReadingRepository
# from app.database.roi_repository import ROIRepository
# from app.database.session_repository import SessionRepository
# from app.models.roi_model import ROIModel
#
#
# def test_create_reading(tmp_path: Path):
#     database_path = tmp_path / "test_app.db"
#
#     database = DatabaseManager(database_path)
#     database.initialize()
#
#     camera_repository = CameraRepository(database)
#     roi_repository = ROIRepository(database)
#     session_repository = SessionRepository(database)
#     reading_repository = ReadingRepository(database)
#
#     camera = camera_repository.create(
#         name="Test Camera",
#         source="0",
#         enabled=False,
#     )
#
#     roi_model = ROIModel(
#         id=0,
#         name="ROI 1",
#         x=10,
#         y=10,
#         width=100,
#         height=50,
#         enabled=True,
#         polling_interval_sec=1,
#     )
#
#     roi_id = roi_repository.create(
#         camera_id=camera.id,
#         roi=roi_model,
#     )
#
#     session_id = session_repository.create("Test Session")
#
#     reading_id = reading_repository.create(
#         session_id=session_id,
#         roi_id=roi_id,
#         value=123.45,
#         raw_text="123,45",
#         confidence=0.95,
#     )
#
#     readings = reading_repository.list_latest(limit=10)
#
#     assert reading_id > 0
#     assert len(readings) == 1
#     assert readings[0]["value"] == 123.45
#     assert readings[0]["raw_text"] == "123,45"