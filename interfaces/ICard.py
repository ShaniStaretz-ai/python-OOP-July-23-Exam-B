from abc import ABC, abstractmethod
class ICard(ABC):
    @property
    @abstractmethod
    def suit(self): pass

    @property
    @abstractmethod
    def rank(self): pass

    @abstractmethod
    def get_display_name(self): pass