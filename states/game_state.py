import pygame
from .state import State
from .board import Board
from .cell import Cell


class GameState(State):
    def __init__(self, screen, width, height, bombs_number=20):
        self.width = width
        self.height = height
        self.board_top = 0
        self.board_left = 0

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


    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.game_board.visit_cell(self.get_clicked_rect_index())
            if event.button == 3:
                self.game_board.mark_cell(self.get_clicked_rect_index())

    def update(self):
        pass

    def render(self):
        self.game_board.draw_board(self.screen)
