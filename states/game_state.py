import pygame
from .state import State
from .board import Board
from .difficulty import Difficulty
from .cell import Cell
from .cell_type import CellType


class GameState(State):
    DISPLAY_SIZE = 2

    def __init__(self, diffculty: Difficulty):
        self.init_board_details(diffculty)
        self.board_top = self.DISPLAY_SIZE * Cell.CELL_SIZE
        self.board_left = Board.BOARD_PADDING

        self.load_fonts()

        self.init_game()
        self.set_screen()
        self.init_layout()
        self.flag_img = pygame.image.load("./assets/flag.png")
        img_size = round(Cell.CELL_SIZE * 1)
        self.flag_img = pygame.transform.scale(self.flag_img, (img_size, img_size))
        self.clock_msg = ""

    def set_screen(self):
        screen_width = 2 * Board.BOARD_PADDING + self.width * Cell.CELL_SIZE
        screen_height = (
            self.DISPLAY_SIZE * Cell.CELL_SIZE
            + self.height * Cell.CELL_SIZE
            + Board.BOARD_PADDING
        )
        super().__init__(pygame.display.set_mode((screen_width, screen_height)))


    def init_board_details(self, diffculty: Difficulty):
        if diffculty == Difficulty.EASY:
            self.width = 10
            self.height = 12
            self.bombs_number = 10
        elif diffculty == Difficulty.MEDIUM:
            self.width = 16
            self.height = 20
            self.bombs_number = 45
        else:
            self.width = 30
            self.height = 20
            self.bombs_number = 99

    def init_layout(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        self.bg_rect = pygame.Rect(0, 0, screen_width, screen_height)
        self.flags_rect = pygame.Rect(
            Board.BOARD_PADDING,
            Board.BOARD_PADDING,
            4 * Cell.CELL_SIZE,
            self.DISPLAY_SIZE * Cell.CELL_SIZE - 2 * Board.BOARD_PADDING,
        )

        self.time_rect = pygame.Rect(
            screen_width - 4 * Cell.CELL_SIZE - Board.BOARD_PADDING,
            Board.BOARD_PADDING,
            4 * Cell.CELL_SIZE,
            self.DISPLAY_SIZE * Cell.CELL_SIZE - 2 * Board.BOARD_PADDING,
        )


    def init_game(self):
        self.game_board = Board(
            self.board_left,
            self.board_top,
            self.width,
            self.height,
            self.bombs_number,
        )
        self.is_win = False
        self.valid_matches = 0
        self.is_game_over = False
        self.left_flags = self.bombs_number
        self.clock = 0

    def load_fonts(self):
        font_location = "./assets/m12.ttf"
        self.header_font = pygame.font.Font(font_location, 31)
        self.subheader_font = pygame.font.Font(font_location, 16)
        self.left_flags_font = pygame.font.Font(font_location, 20)

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

        if self.is_game_over or self.is_win:
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
                self.valid_matches -= 1
        else:
            if self.left_flags == 0:
                return
            self.left_flags -= 1
            selected_cell.type = CellType.FLAGGED

            if selected_cell.is_trap:
                self.valid_matches += 1

            if self.valid_matches == self.bombs_number:
                self.is_win = True

    def show_ending_msg(self, msg):
        msg = msg.upper()
        subheader_msgs = ["Press Space to play again", "or press Q to leave"]
        header_surf = self.header_font.render(msg, True, (255, 255, 255))
        text_rect = header_surf.get_rect(
            center=(
                self.screen.get_width() // 2,
                self.screen.get_height() // 2 - header_surf.get_height() // 2,
            )
        )
        self.screen.blit(header_surf, text_rect)

        for idx, msg in enumerate(subheader_msgs):
            msg_surf = self.subheader_font.render(msg, True, (255, 255, 255))
            msg_rect = msg_surf.get_rect(
                center=(
                    self.screen.get_width() // 2,
                    text_rect.y
                    + 2 * text_rect.height
                    + (msg_surf.get_height() + 5) * idx,
                )
            )
            self.screen.blit(msg_surf, msg_rect)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not (
            self.is_win or self.is_game_over
        ):
            if event.button == 1:
                self.visit_cell(self.get_clicked_rect_index())
            if event.button == 3:
                self.mark_cell(self.get_clicked_rect_index())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (self.is_win or self.is_game_over):
                self.init_game()
            elif event.key == pygame.K_q and (self.is_win or self.is_game_over):
                self.end_state()

    def draw_flags_left(self):
        msg = f"{self.left_flags}"
        flags_txt_surf = self.left_flags_font.render(msg, True, (255, 255, 255))
        offset = (flags_txt_surf.get_width() + self.flag_img.get_width()) // 2

        flag_rect = self.flag_img.get_rect(
            x=self.flags_rect.centerx - offset,
            y=self.flags_rect.centery - self.flag_img.get_height() // 2,
        )
        flags_txt_rect = flags_txt_surf.get_rect(
            x=flag_rect.x + flag_rect.width,
            y=self.flags_rect.centery - flags_txt_surf.get_height() // 2,
        )

        self.screen.blit(self.flag_img, flag_rect)
        self.screen.blit(flags_txt_surf, flags_txt_rect)

    def draw_clock(self):
        msg_surf = self.left_flags_font.render(self.clock_msg, True, (255, 255, 255))
        msg_rect = msg_surf.get_rect(center=(self.time_rect.center))
        self.screen.blit(msg_surf, msg_rect)

    def update(self, fps):
        if not (self.is_win or self.is_game_over):
            self.clock += 1
            self.clock_msg = f"{self.clock//fps}"

    def render(self):
        pygame.draw.rect(self.screen, (32, 32, 32), self.bg_rect)
        pygame.draw.rect(self.screen, Cell.CELL_COLOR_3, self.flags_rect)
        pygame.draw.rect(self.screen, Cell.CELL_COLOR_3, self.time_rect)
        self.draw_flags_left()
        self.draw_clock()

        self.game_board.draw_board(self.screen)
        if self.is_win:
            self.show_ending_msg("You have won")
        if self.is_game_over:
            self.show_ending_msg("You have lost")
