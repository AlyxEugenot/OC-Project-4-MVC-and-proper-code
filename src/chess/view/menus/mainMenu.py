import chess.view.menus._abstract as _abstract
import chess.view.menus.tournamentMenu as tournamentMenu


class MainMenu(_abstract.Menu):
    def __init__(self):
        title = "Menu principal"
        menu_option_name = "Main Menu"
        super().__init__(title, menu_option_name)

        self.tournament_menu = tournamentMenu.WhichTournament()
        self.add_child(self.tournament_menu)
        self.add_child(
            _abstract.Action("Ajouter de nouveaux joueurs", self.ajouter_nouveaux_joueurs)
        )
        self.add_child(_abstract.Action("Consulter les rapports", self.consulter))

    def execute(self):
        return super().execute()


    def ajouter_nouveaux_joueurs(self):
        print("ajouter_nouveaux_joueurs")


    def consulter(self):
        print("consulter")


if __name__ == "__main__":
    menu = MainMenu()
    menu.execute()
