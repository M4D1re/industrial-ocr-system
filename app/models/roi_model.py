from dataclasses import dataclass


@dataclass
class ROIModel:
    """
    Region of interest selected on camera frame.
    """

    id: int
    name: str
    x: int
    y: int
    width: int
    height: int
    enabled: bool = True
    polling_interval_sec: int = 5