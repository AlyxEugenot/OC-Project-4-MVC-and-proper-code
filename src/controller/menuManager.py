import controller
# from view.texts import Text
from menus._menu import Menu

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
        menu: Menu,
        display_condition: bool = True,
    ):
        self.default_order = default_order
        self.desciption = description
        self.menu = menu
        self.display_condition = display_condition


class Arborescence:
    def __init__(self, menus: tuple[Menu]):
        self.menus = menus

    def go_back(self) -> Menu:
        return self.menus[-2]

    def go_root(self) -> Menu:
        return self.menus[0]


class MenuManager:
    def __init__(self, controller: controller.Controller, menu: Menu):
        self.controller = controller
        self.current_menu:Menu = menu
        self.current_menu.controller = self.controller

    def input_handling(self, input: str):
        output = self.regular_inputs(input)
        if output is not None:
            return
        else:
            menu = self.current_menu.resolve_input(input)
            if menu is not None:
                self.current_menu = menu
            else:
                self.current_menu.text_obj.prefix_all_str(f"Wrong input")

    def get_current_arborescence(self) -> Arborescence:
        return self.current_menu.arborescence

    def regular_inputs(self, which_input):
        match which_input:
            case "q":
                # TODO confirm ?
                self.controller.quit()
                # don't return to end the loop (?)
            case "b":
                return self.get_current_arborescence().go_back()
            case "m":
                return self.get_current_arborescence().go_root()
            case _:
                return None
