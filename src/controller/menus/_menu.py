from abc import ABC, abstractmethod
from controller import Controller
from menuManager import Choice, Arborescence
from typing import Self
from view.texts import Text


class Menu(ABC):
    def __init__(
        self,
        text_obj: Text,
        choices: tuple[Choice],
        previous_menu: Self,
    ):
        self.text_obj = text_obj
        self.choices = choices
        self.organize_choices(choices)
        self.arborescence = Arborescence([previous_menu.arborescence, Self])
        self.controller: Controller = previous_menu.controller
        self.loop_by_default = True

    def organize_choices(self, choices: list[Choice]) -> list[Choice]:
        remaining_choices = []
        choices.sort(key=lambda x: x.default_order)
        for choice in choices:
            if choice.display_condition is not None:
                if choice.display_condition() is False:
                    continue
            remaining_choices.append(choice)

        for i, choice in enumerate(remaining_choices):
            choice.default_order = i + 1

    def loop(self):
        while True:
            self.work()

            if self.loop_by_default is False:
                break
            print(
                self.text_obj.prefix_all_str(
                    f"\nBack to {self.text_obj.title} start:\n"
                )
            )

    def resolve_input(self, input: str) -> Self:
        choice_dict = dict([[str(x.default_order), x.menu] for x in self.choices])
        if input in choice_dict.keys():
            return choice_dict[input]
        else:
            return None

    @abstractmethod
    def work(self):
        pass
