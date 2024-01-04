from pygame.event import Event

from states.game_state import GameState

from .difficulty import Difficulty
from .state import State
import pygame


class MenuState(State):
    def __init__(self):
        screen = pygame.display.set_mode((400, 600))
        super().__init__(screen)

        font_location = "./assets/m12.ttf"

        self.title_font = pygame.font.Font(font_location, 30)
        self.regualr_font = pygame.font.Font(font_location, 15)
        self.difficulty_lvl: Difficulty = Difficulty.EASY
        self.init_layout()

    def init_layout(self):
        title_text = "Minesweeper"
        self.title_txt_surf = self.title_font.render(title_text, True, (0, 0, 0))
        self.title_txt_rect = self.title_txt_surf.get_rect(
            center=(self.screen.get_width() // 2, 60)
        )
        mode_label = "Difficulty level: "
        self.mode_label_surf = self.regualr_font.render(mode_label, True, (0, 0, 0))
        self.mode_label_rect = self.mode_label_surf.get_rect(
            centerx=self.screen.get_width() // 2, centery=self.screen.get_height() // 2
        )

        self.update_difficulty()

        self.start_btn = pygame.Rect(
            self.mode_label_rect.left,
            self.mode_rect.bottom + 40,
            self.mode_label_rect.width,
            60,
        )
        start_txt = "Start"

        self.start_surf = self.regualr_font.render(start_txt, True, (255, 255, 255))
        self.start_rect = self.start_surf.get_rect(center=self.start_btn.center)

        self.quit_btn = pygame.Rect(
            self.start_btn.left,
            self.start_btn.bottom + 10,
            self.start_btn.width,
            60,
        )
        quit_text = "Quit"

        self.quit_surf = self.regualr_font.render(quit_text, True, (255, 255, 255))
        self.quit_rect = self.quit_surf.get_rect(center=self.quit_btn.center)

    def update_difficulty(self):
        mode_txt = f"{self.difficulty_lvl.name}"
        self.mode_surf = self.title_font.render(mode_txt, True, (0, 0, 0))
        self.mode_rect = self.mode_surf.get_rect(
            centerx=self.screen.get_width() // 2,
            centery=self.mode_label_rect.centery + self.mode_surf.get_height() + 10,
        )

    def update_triangles(self):
        y1 = self.mode_rect.centery
        y2 = self.mode_rect.top + 5
        y3 = self.mode_rect.bottom - 5
        x_start = self.mode_rect.left - 30
        x_end = self.mode_rect.right + 30

        self.mode_left_vertecies = (
            (x_start, y1),
            (x_start + 10, y2),
            (x_start + 10, y3),
        )
        self.mode_right_verecies = ((x_end, y2), (x_end + 10, y1), (x_end, y3))

        self.mode_left_rect = pygame.Rect(x_start, y2, 10, y3 - y2)
        self.mode_right_rect = pygame.Rect(x_end, y2, 10, y3 - y2)

    def draw_triagnle_btns(self):
        if self.difficulty_lvl.value > 0:
            pygame.draw.polygon(self.screen, (0, 0, 0), self.mode_left_vertecies)
        if self.difficulty_lvl.value < len(Difficulty) - 1:
            pygame.draw.polygon(self.screen, (0, 0, 0), self.mode_right_verecies)

    def handle_events(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.mode_left_rect.collidepoint(mouse_pos):
                if self.difficulty_lvl.value == 0:
                    return
                self.difficulty_lvl = Difficulty(self.difficulty_lvl.value - 1)
            if self.mode_right_rect.collidepoint(mouse_pos):
                if self.difficulty_lvl.value == len(Difficulty) - 1:
                    return
                self.difficulty_lvl = Difficulty((self.difficulty_lvl.value + 1))
            if self.start_btn.collidepoint(mouse_pos):
                self._next_state = GameState(self.difficulty_lvl)
            if self.quit_btn.collidepoint(mouse_pos):
                self.end_state()

    def update(self, fps):
        self.update_difficulty()
        self.update_triangles()

    def render(self):
        self.screen.fill((222, 222, 222))
        self.screen.blit(self.title_txt_surf, self.title_txt_rect)
        self.screen.blit(self.mode_label_surf, self.mode_label_rect)
        self.screen.blit(self.mode_surf, self.mode_rect)
        self.draw_triagnle_btns()

        pygame.draw.rect(self.screen, (0, 0, 0), self.start_btn)
        self.screen.blit(self.start_surf, self.start_rect)

        pygame.draw.rect(self.screen, (201, 68, 68), self.quit_btn)
        self.screen.blit(self.quit_surf, self.quit_rect)

        pass
