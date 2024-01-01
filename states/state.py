import abc

from pygame import Surface
from pygame.event import Event


class State(abc.ABC):
    def __init__(self, screen: Surface):
        self._is_acitve = True
        self.screen = screen
        self._next_state = None

    @property
    def is_acitve(self):
        return self._is_acitve

    @property
    def next_state(self):
        return self._next_state

    def reset_next_state(self):
        self._next_state = None

    def end_state(self):
        self._is_acitve = False

    @abc.abstractmethod
    def handle_events(self, event: Event):
        pass

    @abc.abstractmethod
    def update(self, fps):
        pass

    @abc.abstractmethod
    def render(self):
        pass
