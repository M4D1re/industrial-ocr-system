from dataclasses import dataclass


@dataclass
class CameraModel:
    """
    Camera configuration model.
    """

    id: int

    name: str

    source: str

    enabled: bool = True