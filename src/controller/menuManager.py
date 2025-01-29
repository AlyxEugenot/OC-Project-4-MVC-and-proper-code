import controller
from menus._menu import Menu


class Choices:
    def __init__(
        self, choices: tuple[tuple[str, str, Menu]]
    ):  # input à rentrer, titre de l'input et menu à appeler
        self.choices = dict([[x[0], [x[1], x[2]]] for x in choices])

    def resolve(self, _input: str):
        self.choices[_input][1]()


class Arborescence:
    def __init__(self, menus: tuple[Menu]):
        self.menus = menus

    def go_back(self):
        pass

    def go_deeper(self):
        pass

    def go_root(self):
        pass


class MenuManager:
    def __init__(self, controller: controller.Controller, menu: Menu):
        self.controller = controller
        self.current_menu = menu

    def input_handling(self, input: str, choices: Choices):
        output = self.regular_inputs(input)
        if output is None:
            return
        else:
            self.get_current_arborescence().go_deeper()
            choices.resolve(output)
            pass

    def get_current_arborescence(self)->Arborescence:
        return self.current_menu.arborescence

    def regular_inputs(self, which_input):
        match which_input:
            case "q":
                # TODO confirm ?
                self.controller.quit()
            case "b":
                self.get_current_arborescence().go_back()
            case "m":
                self.get_current_arborescence().go_root()
            case _:
                return None

    def back(self):
        self.arborescence.go_back()
        pass
