from enum import Enum

class CellType(Enum):
    UNCHECKED = 1
    CHECKED = 2
    BOMB = 3
    FLAGGED = 5
