import pygame
from .state import State
from .board import Board
from .cell import Cell
from .cell_type import CellType


class GameState(State):
    def __init__(self, screen, width, height, bombs_number=20):
        self.width = width
        self.height = height
        self.board_top = 0
        self.board_left = 0
        self.is_game_over = False
        self.valid_matches = 0
        self.bombs_number = bombs_number

        self.left_flags = bombs_number

        self.game_board = Board(
            self.board_left, self.board_top, self.width, self.height, bombs_number
        )

        screen = pygame.display.set_mode(
            (width * Cell.CELL_SIZE, height * Cell.CELL_SIZE)
        )

        super().__init__(screen)

    def get_clicked_rect_index(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_x = mouse_x - self.board_left
        mouse_y = mouse_y - self.board_top

        row = mouse_y // Cell.CELL_SIZE
        col = mouse_x // Cell.CELL_SIZE

        index = row * self.width + col

        return index

    def visit_cell(self, cell_index):
        if cell_index < 0 or cell_index > self.width * self.height:
            return
        selected_cell = self.game_board.board[cell_index]

        if self.is_game_over:
            return

        if (
            selected_cell.type == CellType.CHECKED
            or selected_cell.type == CellType.FLAGGED
        ):
            return
        if selected_cell.is_trap:
            self.is_game_over = True
            self.game_board.reveal_bombs()
            return

        selected_cell.type = CellType.CHECKED

        if selected_cell.bomb_count == 0:
            self.visit_neighbours(cell_index)

    def visit_neighbours(self, cell_index):
        if c := self.game_board.get_n_neighbour(self.game_board.board[cell_index]):
            self.visit_cell(c.index)
        if c := self.game_board.get_ne_neighbour(self.game_board.board[cell_index]):
            self.visit_cell(c.index)
        if c := self.game_board.get_e_neighbour(self.game_board.board[cell_index]):
            self.visit_cell(c.index)
        if c := self.game_board.get_se_neighbour(self.game_board.board[cell_index]):
            self.visit_cell(c.index)
        if c := self.game_board.get_s_neighbour(self.game_board.board[cell_index]):
            self.visit_cell(c.index)
        if c := self.game_board.get_sw_neighbour(self.game_board.board[cell_index]):
            self.visit_cell(c.index)
        if c := self.game_board.get_w_neighbour(self.game_board.board[cell_index]):
            self.visit_cell(c.index)
        if c := self.game_board.get_nw_neighbour(self.game_board.board[cell_index]):
            self.visit_cell(c.index)

    def mark_cell(self, cell_index):
        if cell_index < 0 or cell_index > self.width * self.height:
            return
        selected_cell = self.game_board.board[cell_index]

        if selected_cell.type == CellType.FLAGGED:
            selected_cell.type = CellType.UNCHECKED
            self.left_flags += 1
            if selected_cell.is_trap:
                self.valid_matches-=1
        else:
            if self.left_flags == 0:
                return
            self.left_flags -= 1
            selected_cell.type = CellType.FLAGGED

            if selected_cell.is_trap:
                self.valid_matches+=1
        self.check_win()

    def check_win(self):
        if self.valid_matches == self.bombs_number:
            print("wygrałeś")


    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.visit_cell(self.get_clicked_rect_index())
            if event.button == 3:
                self.mark_cell(self.get_clicked_rect_index())

    def update(self):
        pass

    def render(self):
        self.game_board.draw_board(self.screen)
