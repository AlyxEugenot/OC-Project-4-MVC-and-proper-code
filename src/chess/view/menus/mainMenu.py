import chess.view.menus._abstract as _abstract
import chess.view.menus.tournamentMenu as tournamentMenu
import chess.view.menus.addPlayersMenu as addPlayersMenu
import chess.view.menus.reportsMenu as reportsMenu


class MainMenu(_abstract.Menu):
    def __init__(self):
        title = "Menu principal"
        super().__init__(title=title)

        self.add_child(tournamentMenu.WhichTournament())
        self.add_child(addPlayersMenu.AddPlayers())
        self.add_child(reportsMenu.Reports())


if __name__ == "__main__":
    menu = MainMenu()
    menu.execute()
