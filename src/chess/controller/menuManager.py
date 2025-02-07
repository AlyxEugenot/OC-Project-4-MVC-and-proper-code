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
        self.current_menu.controller = self.controller

    def get_current_arborescence(self) -> "Arborescence":
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
