from pydantic import BaseModel


class LoggingConfig(BaseModel):
    level: str = "INFO"
    filename: str = "application.log"
    max_file_size_mb: int = 10
    backup_count: int = 5


class DatabaseConfig(BaseModel):
    filename: str = "app.db"


class UIConfig(BaseModel):
    theme: str = "dark"
    window_width: int = 1600
    window_height: int = 900


class AppConfig(BaseModel):
    app_name: str = "Industrial OCR System"
    app_version: str = "0.1.0"

    logging: LoggingConfig = LoggingConfig()
    database: DatabaseConfig = DatabaseConfig()
    ui: UIConfig = UIConfig()