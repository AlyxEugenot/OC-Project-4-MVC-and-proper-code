import view
import controller

quitapp = False


def main_menu():
    quit_menu = False
    while not quit_menu:
        view.context.intro(
            "Main Menu:\n"
        )  # Faire une fonction qui affiche tout le temps le contexte où se trouve l'utilisateur
        view.intro()  # click.echo(f"{self.intro}Main menu stuff, 1 to tournament shit, 2 to player stuff...")
        user_input = view.input.ask_prompt(
            "Choose option"
        )  # click.prompt("Choose option")
    first_choice = view.ask_prompt()

    # match first_choice:


if __name__ == "__main__":
    controller.Controller.main()
