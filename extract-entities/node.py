from datetime import datetime
from typing import Tuple

class Node:
    def __init__(self, time: datetime, location: str, coordinates: Tuple[float, float], description: str):
        self.time = time
        self.location = location
        self.coordinates = coordinates
        self.description = description


