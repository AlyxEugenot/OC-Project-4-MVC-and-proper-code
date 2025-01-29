from abc import ABC, abstractmethod
from menuManager import Choices, Arborescence
from typing import Self


class Menu(ABC):
    def __init__(self, choices: Choices, previous_menu:Self):
        self.choices = choices
        self.arborescence = Arborescence([previous_menu.arborescence, Self])
        pass

    @abstractmethod
    def work(self, *args):
        pass
