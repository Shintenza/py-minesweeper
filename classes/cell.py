from enums.cell_type import CellType
from pygame import Rect, Surface, draw


class Cell:
    """single cell later held in a array of cells in Board class. Implements 
    static methods that renders cell at given position and state."""

    CELL_COLOR_1 = (111, 86, 83)
    CELL_COLOR_2 = (24, 24, 24)
    CELL_COLOR_3 = (51, 51, 51)

    CELL_COLOR_4 = (78, 47, 35)
    CELL_COLOR_5 = (45, 23, 16)

    CELL_SIZE = 40
    OFFSET = 2

    def __init__(self, index: int, is_trap=False):
        self._index = index
        self._type = CellType.UNCHECKED
        self._rect = None
        self._is_trap = is_trap
        self._bomb_count = 0

    @property
    def bomb_count(self):
        return self._bomb_count

    @bomb_count.setter
    def bomb_count(self, new_value: int):
        self._bomb_count = new_value

    @property
    def is_trap(self):
        return self._is_trap

    @property
    def index(self):
        return self._index

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type: CellType):
        self._type = new_type

    @classmethod
    def draw_unchecked_cell(cls, screen, left, top, width):
        bg_rect = Rect(left, top, width, width - cls.OFFSET)
        bg_rect_shade = Rect(
            left + cls.OFFSET, top + cls.OFFSET, width - cls.OFFSET, width - cls.OFFSET
        )
        top_rect = Rect(
            left + cls.OFFSET,
            top + cls.OFFSET,
            width - 2 * cls.OFFSET,
            width - 2 * cls.OFFSET,
        )

        draw.rect(screen, cls.CELL_COLOR_1, bg_rect)
        draw.rect(screen, cls.CELL_COLOR_2, bg_rect_shade)
        draw.rect(screen, cls.CELL_COLOR_3, top_rect)

    @classmethod
    def draw_flagged_cell(cls, screen: Surface, flag_img: Surface, left, top, width):
        cls.draw_unchecked_cell(screen, left, top, width)
        flag_rect = flag_img.get_rect(center=(left + width // 2, top + width // 2))
        screen.blit(flag_img, flag_rect)

    @classmethod
    def draw_bomb_cell(cls, screen: Surface, bomb_img: Surface, left, top, width):
        cls.draw_checked_cell(screen, None, 0, left, top, width)
        bomb_rect = bomb_img.get_rect(center=(left + width // 2, top + width // 2))
        screen.blit(bomb_img, bomb_rect)

    @classmethod
    def draw_checked_cell(cls, screen, font, b_count, left, top, width):
        bg_rect = Rect(left, top, width, width)
        top_rect = Rect(
            left + cls.OFFSET,
            top + cls.OFFSET,
            width - 2 * cls.OFFSET,
            width - 2 * cls.OFFSET,
        )

        draw.rect(screen, cls.CELL_COLOR_4, bg_rect)
        draw.rect(screen, cls.CELL_COLOR_5, top_rect)

        if b_count > 0:
            text = f"{b_count}"
            text_surf = font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(left + width // 2, top + width // 2))
            screen.blit(text_surf, text_rect)
