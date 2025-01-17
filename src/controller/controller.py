"""Docstring to come"""  # TODO

import view
import model
import generate
import mainMenu


class Controller:
    quitapp = False
    view = view.View

    def regular_inputs(self, which_input):
        match which_input:
            case "q":
                self.quit()
                # sys.exit(0)
            case "b":
                self.back()
            case _:
                return

    def quit(self):
        self.quitapp = True

    def back(self):
        pass

    def main():
        while True:
            mainMenu.main_menu()
        pass


if __name__ == "__main__":
    Controller.main()
    # créer/lancer un tournoi
    # créer/lancer un round
    # "créer" un match
