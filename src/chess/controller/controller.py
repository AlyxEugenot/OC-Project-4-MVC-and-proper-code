"""Docstring to come"""  # TODO

# import model
# import generate
from chess.controller.menus import MainMenu
from chess.controller.menuManager import MenuManager
from chess.view import View



class Controller:
    def __init__(self, view: View):
        self.quitapp = False
        self.menu_handler: MenuManager = None
        self.view = view

    def quit(self):
        # self.menu_handler.current_menu.text_obj.prefix_all_str("Quitting...")
        self.quitapp = True
        # sys.exit(0)

    def run(self):
        while self.quitapp is False:
            self.menu_handler.current_menu.loop()
            
            if self.menu_handler.next_menu != self.menu_handler.current_menu:
                self.menu_handler.current_menu = self.menu_handler.next_menu
                continue
            
            self.menu_handler.current_menu = (
                self.menu_handler.current_menu.arborescence.go_back()
            )

    def start(self):
        self.menu_handler = MenuManager(self, MainMenu(self))
        self.run()


def execute_program():
    app = Controller(view=View())
    app.start()
    # créer/lancer un tournoi
    # créer/lancer un round
    # "créer" un match


if __name__ == "__main__":
    execute_program()
