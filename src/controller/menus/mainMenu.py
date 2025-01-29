import view
import controller
import view.texts
from _menu import Menu

class MainMenu(Menu):
    quit_menu = False
    while not quit_menu:
        view.context()
        view.intro(view.texts.t_main_menu_options)
        user_input = view.inputs.ask_prompt(
            "Choose option: "
        ) 
        if user_input == "1":
            pass

        # match "1":


if __name__ == "__main__":
    controller.Controller.start()
