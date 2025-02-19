# import view
# import view.texts
from chess.controller.menus._menu import Menu, TextItem, Choice, Arborescence
from typing import TYPE_CHECKING

from chess.controller.menus.tournament import CreateTournamentMenu

if TYPE_CHECKING:
    import controller

m_menu = "menu"


class MainMenu(Menu):
    def __init__(self, controller: "controller.Controller"):
        text_items = {
            m_menu: TextItem(
                "\nBonjour,\n\nStats du menu sur l'état du programme\n",
                [
                    Choice(
                        default_order=1,
                        description="Continuer un tournoi en cours",
                        invoke=lambda: self.continue_tournament(),
                        display_condition=self.display_continue_tournament_bool(),
                    ),
                    Choice(
                        default_order=2,
                        description="Créer un nouveau tournoi",
                        invoke=lambda: self.create_tournament(),
                    ),
                    Choice(
                        default_order=3,
                        description="Ajouter de nouveaux joueurs",
                        invoke=lambda: self.create_players(),
                    ),
                    Choice(
                        default_order=4,
                        description="Consulter les rapports",
                        invoke=lambda: self.show_reports(),
                    ),
                ],
            )
        }
        super().__init__(
            title="Main Menu",
            previous_menu=None,
            text_items=text_items,
            loop_item_by_default=True,
        )
        self.arborescence = Arborescence([MainMenu])
        self.controller = controller
        self.view = controller.view

    def work(self):
        # view.context()
        # view.intro(view.texts.MainMenu())
        self.my_print(self.text_items[m_menu])
        self.my_print(self.text_items[m_menu].choices_str())

        user_input = self.controller.view.input("\t-> ")

        menu= self.resolve_input(user_input, self.text_items[m_menu].choices)
        self.next_menu(menu)

    def display_continue_tournament_bool(self) -> bool:
        # TODO check if any tournament is opened and not yet closed
        return False  # FIXME

    def turn_off_loop(self):  # FIXME delete this, it was for a single lambda test
        self.loop_by_default = False

    def continue_tournament(self):
        # afficher les tournois possibles de continuer
        pass

    def create_tournament(self):
        return CreateTournamentMenu
        pass

    def create_players(self):
        pass

    def show_reports(self):
        pass


if __name__ == "__main__":
    import chess

    a = MainMenu(chess.Controller(chess.View()))
    a.controller.start()
