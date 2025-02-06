# import view
# import view.texts
from ._menu import Menu, Choice
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import controller

class MainMenu(Menu):
    def __init__(self, controller: "controller.Controller"):
        display_continue_tournament_condition = self.display_continue_tournament_bool()
        choices = [
            Choice(
                default_order=1,
                description="Continuer le tournoi précédent",
                menu=None,
                display_condition=display_continue_tournament_condition,
            ),
            Choice(default_order=2, description="Créer un nouveau tournoi", menu=None),
            Choice(
                default_order=3, description="Ajouter de nouveaux joueurs", menu=None
            ),
            Choice(default_order=4, description="Consulter les rapports", menu=None),
        ]
        super().__init__(
            title="Main Menu",
            choices=choices,
            previous_menu=None, # override in next step, this is too avoid error
        )
        self.arborescence = [MainMenu]
        self.controller = controller

    def work(self):        
        # view.context()
        # view.intro(view.texts.MainMenu())
        user_input = input("input:")#view.inputs.ask_prompt("Choose option: ")
        
        new_menu=self.resolve_input(user_input)

    def display_continue_tournament_bool(self) -> bool:
        # TODO check if any tournament is opened and not yet closed
        return True #FIXME

if __name__ == "__main__":
    _controller = controller.Controller
    a = MainMenu([Choice(1,"a", None),Choice(2,"b", None),Choice(6,"aze", None)],_controller)
    a.text_obj.title
    a.choices[1].menu.text_obj.title
