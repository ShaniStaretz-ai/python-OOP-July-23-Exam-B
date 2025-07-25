from abc import ABC, abstractmethod
class IDeck(ABC):
    @property
    @abstractmethod
    def cards(self): pass

    @abstractmethod
    def shuffle(self): pass

    @abstractmethod
    def draw(self): pass

    @abstractmethod
    def add_card(self, card): pass