import pygame
from states.menu_state import MenuState
from states.state import State
from states.game_state import GameState


class Game:
    FPS = 60

    def __init__(self):
        self.states_stack: list[State] = []
        self.is_finished = False
        pygame.font.init()

        self.clock = pygame.time.Clock()
        self.states_stack.append(MenuState())

    def play(self):
        pygame.init()

        while not self.is_finished:
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_finished = True
            else:
                if len(self.states_stack) > 0:
                    self.states_stack[-1].handle_events(event)

    def update(self):
        self.handle_events()
        if len(self.states_stack) > 0:
            if not self.states_stack[-1].is_acitve:
                self.states_stack.pop()
                if len(self.states_stack) > 0:
                    self.states_stack[-1].set_screen()
                return
            if self.states_stack[-1].next_state:
                state_to_append = self.states_stack[-1].next_state
                self.states_stack[-1].reset_next_state()
                self.states_stack.append(state_to_append)

            self.states_stack[-1].update(self.FPS)

    def render(self):
        if len(self.states_stack) == 0:
            self.is_finished = True
            return
        self.states_stack[-1].render()
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.play()
