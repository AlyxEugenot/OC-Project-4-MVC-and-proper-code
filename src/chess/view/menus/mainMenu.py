import chess.view.menus._abstract as _abstract
import chess.view.menus.tournamentMenu as tournamentMenu
import chess.view.menus.addPlayersMenu as addPlayersMenu


class MainMenu(_abstract.Menu):
    def __init__(self):
        title = "Menu principal"
        super().__init__(title)

        self.add_child(tournamentMenu.WhichTournament())
        self.add_child(addPlayersMenu.AddPlayers())
        self.add_child(_abstract.Action("Consulter les rapports", self.consulter))

    def execute(self):
        return super().execute()

    def consulter(self):
        print("consulter")


if __name__ == "__main__":
    menu = MainMenu()
    menu.execute()
