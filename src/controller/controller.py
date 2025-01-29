"""Docstring to come"""  # TODO

from view import View
import model
import generate
import src.controller.menus.mainMenu as mainMenu
from menuManager import MenuManager


# region GPT
######################################################### exemple de nested loop #########################################################
class Program:
    def __init__(self):
        self.running = True
        self.in_nested_loop = False

    def handle_input(self, user_input):
        if user_input == "b" and self.in_nested_loop:
            print("Returning to the main loop.")
            self.in_nested_loop = False
            return "break"
        elif user_input == "quit":
            print("Exiting program.")
            self.running = False
        else:
            print(f"Input handled: {user_input}")

    def main_loop(self):
        while self.running:
            user_input = input("Main Loop > ")
            if user_input == "go":
                print("Entering nested loop.")
                self.in_nested_loop = True
                self.nested_loop()
            else:
                self.handle_input(user_input)

    def nested_loop(self):
        while self.in_nested_loop:
            user_input = input("Nested Loop > ")
            if self.handle_input(user_input) == "break":
                break


if __name__ == "__main__":
    program = Program()
    program.main_loop()

######################################### exemple d'accès aux valeurs de la classe au-dessus dans la classe en dessous #########################################


class A:
    def __init__(self, value):
        self.value = value
        self.b_instance = B(self)  # Pass the instance of A to B


class B:
    def __init__(self, parent: A):
        self.parent = parent  # Store the reference to the instance of A

    def access_a_value(self):
        return self.parent.value  # Access a value from A


# Instantiate A
a_instance = A(42)

# Access class A's value through class B
print(a_instance.b_instance.access_a_value())  # Output: 42

# endregion


class Controller:
    def __init__(self, view: View):
        self.quitapp = False
        self.menu_handler = MenuManager(self,mainMenu)
        self.view = view
        self.view.controller=self

    def quit(self):
        self.quitapp = True
        # sys.exit(0)

    def run(self):
        while self.quitapp is False:
            self.menu_handler.current_menu.work()
        
    def start(self):
        while self.quitapp is False:
            mainMenu.main_menu()


if __name__ == "__main__":
    app = Controller(view=View)
    app.start()
    # créer/lancer un tournoi
    # créer/lancer un round
    # "créer" un match
