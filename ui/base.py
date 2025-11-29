from abc import ABC, abstractmethod
class Base(ABC):

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def handle_end_game(self):
        pass

    @abstractmethod
    def on_submit(self, letter: str):
        pass