from typing import List

from pygame import Surface, image, transform, font
from classes.cell import Cell
from enums.cell_type import CellType
import random


class Board:
    GAP_SIZE = 1
    BOARD_PADDING = 10
    def __init__(self, left: int, top: int, width: int, height: int, bombs_number: int):
        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self.bombs_number = bombs_number

        self.load_assets()
        self.init_board()
        self.numerate_board()


    def init_board(self):
        self.bomb_positions = random.sample(
            range(0, self.width * self.height), self.bombs_number
        )
        self.board: List[Cell] = []

        for i in range(self.width * self.height):
            if i in self.bomb_positions:
                self.board.append(Cell(i, True))
            else:
                self.board.append(Cell(i))

    def load_assets(self):
        self.num_font = font.Font('./assets/m12.ttf', 16)

        self.flag_img = image.load("./assets/flag.png")
        img_size = round(Cell.CELL_SIZE * 0.75)
        self.flag_img = transform.scale(self.flag_img, (img_size, img_size))

        self.bomb_img = image.load('./assets/bomb.png')
        self.bomb_img = transform.scale(self.bomb_img, (img_size, img_size))

    def reveal_bombs(self):
        for bomb_index in self.bomb_positions:
            bomb_cell = self.board[bomb_index]

            bomb_cell.type = CellType.CHECKED

    def numerate_board(self):
        for i in range(len(self.board)):
            current_cell = self.board[i]

            if (c := self.get_n_neighbour(current_cell)) and c.is_trap:
                current_cell.bomb_count += 1
            if (c := self.get_ne_neighbour(current_cell)) and c.is_trap:
                current_cell.bomb_count += 1
            if (c := self.get_e_neighbour(current_cell)) and c.is_trap:
                current_cell.bomb_count += 1
            if (c := self.get_se_neighbour(current_cell)) and c.is_trap:
                current_cell.bomb_count += 1
            if (c := self.get_s_neighbour(current_cell)) and c.is_trap:
                current_cell.bomb_count += 1
            if (c := self.get_sw_neighbour(current_cell)) and c.is_trap:
                current_cell.bomb_count += 1
            if (c := self.get_w_neighbour(current_cell)) and c.is_trap:
                current_cell.bomb_count += 1
            if (c := self.get_nw_neighbour(current_cell)) and c.is_trap:
                current_cell.bomb_count += 1

    def get_n_neighbour(self, cell: Cell):
        if cell.index < self.width:
            return None
        return self.board[cell.index - self.width]

    def get_ne_neighbour(self, cell: Cell):
        if (cell.index + 1) % (self.width) == 0 or cell.index < self.width:
            return None
        return self.board[cell.index - (self.width - 1)]

    def get_e_neighbour(self, cell: Cell):
        if (cell.index + 1) % self.width == 0:
            return None
        return self.board[cell.index + 1]

    def get_se_neighbour(self, cell: Cell):
        if (
            cell.index + 1
        ) % self.width == 0 or cell.index // self.width == self.height - 1:
            return None
        return self.board[cell.index + self.width + 1]

    def get_s_neighbour(self, cell: Cell):
        if cell.index // self.width == self.height - 1:
            return None
        return self.board[cell.index + self.width]

    def get_sw_neighbour(self, cell: Cell):
        if cell.index % self.width == 0 or cell.index // self.width == self.height - 1:
            return None
        return self.board[cell.index + self.width - 1]

    def get_w_neighbour(self, cell: Cell):
        if cell.index % self.width == 0:
            return None
        return self.board[cell.index - 1]

    def get_nw_neighbour(self, cell: Cell):
        if cell.index % self.width == 0 or cell.index < self.width:
            return None
        return self.board[cell.index - self.width - 1]



    def draw_board(self, screen: Surface):
        for i in range(self.width * self.height):
            current_cell = self.board[i]
            col = i % self.width
            row = i // self.width

            rect_x = self.left + col * Cell.CELL_SIZE
            rect_y = self.top + row * Cell.CELL_SIZE

            if (
                current_cell.type == CellType.UNCHECKED
                # and not current_cell.is_trap
            ):
                Cell.draw_unchecked_cell(screen, rect_x, rect_y, Cell.CELL_SIZE)
            if current_cell.type == CellType.CHECKED:
                if current_cell.is_trap:
                    Cell.draw_bomb_cell(screen, self.bomb_img, rect_x, rect_y, Cell.CELL_SIZE)
                else:
                    Cell.draw_checked_cell(screen, self.num_font, current_cell.bomb_count, rect_x, rect_y, Cell.CELL_SIZE)


            if current_cell.type == CellType.FLAGGED:
                Cell.draw_flagged_cell(
                    screen, self.flag_img, rect_x, rect_y, Cell.CELL_SIZE
                )
