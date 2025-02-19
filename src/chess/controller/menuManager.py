# from view.texts import Text
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .menus import Menu, Arborescence
if TYPE_CHECKING:
    from controller import Controller


class MenuManager:
    def __init__(self, controller: "Controller", menu: "Menu"):
        self.controller = controller
        self.current_menu:"Menu" = menu
        self.next_menu:"Menu"=None

    def regular_inputs(self, which_input:str):
        match which_input:
            case "q":
                # TODO confirm ?
                self.controller.quit()
                # don't return to end the loop (?)
            case "b":
                return self.current_menu.arborescence.go_back()
            case "m":
                return self.current_menu.arborescence.go_root()
            case _:
                return None
    def set_next_menu(self):
        self.current_menu= self.next_menu
        self.current_menu.controller = self.controller
        