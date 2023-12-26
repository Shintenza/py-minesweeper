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
        self.states_stack.append(GameState(self.screen, 10, 15))

    def play(self):
        pygame.init()

        while not self.is_finished:
            self.render()
            self.update()

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
        self.states_stack[-1].update()

        if (len(self.states_stack) and self.states_stack[-1].is_acitve):
            self.states_stack[-1].update()
        else:
            self.states_stack.pop()

    def render(self):
        self.screen.fill((0, 0, 0))
        if len(self.states_stack) == 0:
            self.is_finished = True
            return
        self.states_stack[-1].render()

        pygame.display.flip()
        self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = Game()
    game.play()
