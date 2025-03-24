import chess.view.menus._abstract as _abstract
import chess.view.menus.tournamentMenu as tournamentMenu
import chess.view.menus.addPlayersMenu as addPlayersMenu
import chess.view.menus.reportsMenu as reportsMenu

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chess.controller.app import Context


class MainMenu(_abstract.Menu):
    def __init__(self, context: "Context"):
        title = "Menu principal"
        super().__init__(title=title)
        self.context = context

        self.add_child(tournamentMenu.WhichTournament())
        self.add_child(addPlayersMenu.AddPlayers())
        self.add_child(reportsMenu.Reports())

        self.tournament = tournamentMenu.TournamentHandling()
        # set up tournament parent relationship
        self.add_child(self.tournament)
        self.children.remove(self.tournament)


if __name__ == "__main__":
    import chess.controller.app

    app = chess.controller.app.App()
    app.view_main_menu.execute()
