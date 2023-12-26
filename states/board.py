from typing import List

from pygame import Surface, image, transform
from .cell import Cell
from .cell_type import CellType
import random


class Board:
    GAP_SIZE = 1

    def __init__(self, left: int, top: int, width: int, height: int, bombs_number: int):
        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self.bombs_number = bombs_number

        self.load_flag_img()
        self.init_board()

    def init_board(self):
        bomb_positions = random.sample(
            range(0, self.width * self.height), self.bombs_number
        )
        self.board: List[Cell] = []

        for i in range(self.width * self.height):
            if i in bomb_positions:
                self.board.append(Cell(i, CellType.BOMB))
            else:
                self.board.append(Cell(i))

    def load_flag_img(self):
        self.flag_img = image.load("./assets/flag.png")
        flag_size = round(Cell.CELL_SIZE * 0.75)
        self.flag_img = transform.scale(self.flag_img, (flag_size, flag_size))

    def visit_cell(self, cell_index):
        if cell_index < 0 or cell_index > self.width * self.height:
            return
        selected_cell = self.board[cell_index]
        selected_cell.type = CellType.CHECKED

    def mark_cell(self, cell_index):
        if cell_index < 0 or cell_index > self.width * self.height:
            return
        selected_cell = self.board[cell_index]
        selected_cell.type = CellType.FLAGGED

    def draw_board(self, screen: Surface):
        for i in range(self.width * self.height):
            current_cell = self.board[i]
            col = i % self.width
            row = i // self.width

            rect_x = self.left + col * Cell.CELL_SIZE
            rect_y = self.top + row * Cell.CELL_SIZE

            if (
                current_cell.type == CellType.UNCHECKED
                or current_cell.type == CellType.BOMB
            ):
                Cell.draw_unchecked_cell(screen, rect_x, rect_y, Cell.CELL_SIZE)
            if current_cell.type == CellType.CHECKED:
                Cell.draw_checked_cell(screen, rect_x, rect_y, Cell.CELL_SIZE)

            if current_cell.type == CellType.FLAGGED:
                Cell.draw_flagged_cell(
                    screen, self.flag_img, rect_x, rect_y, Cell.CELL_SIZE
                )
