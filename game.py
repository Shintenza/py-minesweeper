import pygame
from states.state import State
from states.game_state import GameState


class Game:
    FPS = 60

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.states_stack: list[State] = []
        self.is_finished = False

        self.clock = pygame.time.Clock()
        self.states_stack.append(GameState(10, 15))

    def play(self):
        pygame.init()

        while not self.is_finished:
            self.render()
            self.update()
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
                return
            self.states_stack[-1].update(self.FPS)

    def render(self):
        self.screen.fill((0, 0, 0))
        if len(self.states_stack) == 0:
            self.is_finished = True
            return
        self.states_stack[-1].render()
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.play()
