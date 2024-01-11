from enum import Enum


class CellType(Enum):
    "enum representing different visual states of the cell"
    UNCHECKED = 1
    CHECKED = 2
    FLAGGED = 3
