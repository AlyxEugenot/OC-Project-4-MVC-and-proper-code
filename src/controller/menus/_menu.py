from abc import ABC, abstractmethod
from typing import Self
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller.controller import Controller


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
        default_order: int,
        description: str,
        menu: "Menu",
        display_condition: bool = True,
    ):
        self.default_order = default_order
        self.desciption = description
        self.menu = menu
        self.display_condition = display_condition
    
    def __repr__(self):
        return f"{self.default_order} > {self.menu} : {self.desciption}"


class Arborescence:
    def __init__(self, menus: tuple["Menu"]):
        self.menus = menus

    def go_back(self) -> "Menu":
        return self.menus[-2]

    def go_root(self) -> "Menu":
        return self.menus[0]


class Menu(ABC):
    def __init__(
        self,
        previous_menu: Self,
        choices: tuple[Choice],
        title:str,
        # text_collection va probablement devenir un dict qui contient 
        # 1 - paragraph
        # 2 - choices
        # 3 - les inputs (OU au choix entre choices et inputs OU input est un choices en 1)
        text_collection : dict[str:str]={"paragraph":"/!\\ not implemented"}, 
        loop_by_default:bool=True
    ):
        self.title = title
        self.text_collection = text_collection
        self.choices = choices
        self.organize_choices(choices)
        self.arborescence = Arborescence([previous_menu.arborescence, Self])
        self.controller: "Controller" = previous_menu.controller
        self.loop_by_default = loop_by_default

    def organize_choices(self, choices: list[Choice]) -> list[Choice]:
        remaining_choices = []
        choices.sort(key=lambda x: x.default_order)
        for choice in choices:
            if choice.display_condition is False:
                continue
            remaining_choices.append(choice)

        for i, choice in enumerate(remaining_choices):
            choice.default_order = i + 1

    def loop(self):
        while True:
            self.work()

            if self.loop_by_default is False:
                break
            # print(
            #     self.text_obj.prefix_all_str(
            #         f"\nBack to start of {self.text_obj.title}\n"
            #     )
            # )

    def resolve_input(self, input: str) -> Self:
        choice_dict = dict([[str(x.default_order), x.menu] for x in self.choices])
        if input in choice_dict.keys():
            return choice_dict[input]
        else:
            return None

    @abstractmethod
    def work(self):
        pass
