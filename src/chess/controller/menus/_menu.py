from abc import ABC, abstractmethod
from typing import Self
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chess import Controller, View


# TODO je viens d'enlever les options aux textes (j'organisais ce qui s'affichait ou non là-bas)
# TODO à la place, je vais faire ce travail dans le controller

# TODO il faut que je commence à écrire vraiment comment afficher et utiliser le menu principal
# TODO pour savoir par quelle fonction et à quel endroit du programme accéder aux données
#      (et où on gère "l'affichage selon")
# TODO donc j'utilise et je décide comment les utiliser
# TODO Les endroits sont:
#  - ici
#  - controller.py
#  - texts (avec options)
# a


class Choice:
    def __init__(
        self,
        default_order: int=1,
        description: str="Description",
        invoke: callable = None,
        # menu: "Menu" = None,
        display_condition: bool = True,
    ):
        self.default_order = default_order
        self.desciption = description
        self.invoke = invoke
        # self.menu = menu
        self.display_condition = display_condition

    def __str__(self):
        return f"{self.default_order} > {self.desciption}"

    def __repr__(self):
        return str(self)
        return f"{self.default_order} > {self.menu} : {self.desciption}"


class Arborescence:
    def __init__(self, menus: tuple["Menu"]):
        self.menus = menus

    def go_back(self) -> "Menu":
        if len(self.menus) > 1:
            return self.menus[-2]#(self) #FIXME test
        else:
            return self.menus[0]

    def go_root(self) -> "Menu":
        return self.menus[0]


class Menu(ABC):
    def __init__(
        self,
        previous_menu: Self,
        title: str,
        text_items: dict[str : tuple[str, tuple[Choice]]] = {
            "paragraph": ["/!\\ not implemented", Choice(1, "choice not implemented")]
        },
        loop_item_by_default: bool = True,
    ):
        self.title = title
        self.loop_item_by_default = loop_item_by_default
        self.text_items = text_items
        for key, item in self.text_items.items():
            self.text_items[key][1] = self.organize_choices(item[1])

        if previous_menu is not None:  # for first menu
            self.arborescence = Arborescence([previous_menu.arborescence.menus, Self])
            self.controller: "Controller" = previous_menu.controller
            self.view: "View" = previous_menu.view

    def organize_choices(
        self, choices: list[Choice]
    ) -> list[Choice]:  # TODO implement one item choices
        remaining_choices = []
        choices.sort(key=lambda x: x.default_order)
        for choice in choices:
            if choice.display_condition is False:
                continue
            remaining_choices.append(choice)

        for i, choice in enumerate(remaining_choices):
            choice.default_order = i + 1
        return remaining_choices

    def loop(self):
        while True:
            self.work()

            if self.loop_item_by_default is False:
                break
            # print(
            #     self.text_obj.prefix_all_str(
            #         f"\nBack to start of {self.text_obj.title}\n"
            #     )
            # )

    def resolve_input(self, input: str, choices: tuple[Choice]) -> callable:
        output = self.controller.menu_handler.regular_inputs(input)
        if output is not None:
            return self.null
        else:
            choice_dict = dict([[str(x.default_order), x.invoke] for x in choices])
            if input in choice_dict.keys():
                return choice_dict[input]
            else:
                return self.null

    @abstractmethod
    def work(self):
        pass
    
    def null(self):
        pass
