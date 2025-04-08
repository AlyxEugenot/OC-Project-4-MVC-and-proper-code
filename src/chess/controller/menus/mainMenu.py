import chess.controller.menus._abstract as _abstract
import chess.controller.menus.tournamentMenu as tournamentMenu
import chess.controller.menus.addPlayersMenu as addPlayersMenu
import chess.controller.menus.reportsMenu as reportsMenu

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chess.controller.app import Context
    from chess.view import View


class MainMenu(_abstract.Menu):
    def __init__(self, context: "Context", view: "View"):
        title = "Menu principal"
        super().__init__(title=title)
        self.context = context
        self.view = view

        self.add_child(tournamentMenu.WhichTournament())
        self.add_child(addPlayersMenu.AddPlayers())
        self.add_child(reportsMenu.Reports())

        # set up tournament parent relationship
        self.tournament = self.invisible_child = self.add_remanent_menu_not_child(
            tournamentMenu.TournamentHandling()
        )

        self.late_init(am_root=True)


if __name__ == "__main__":
    import chess.controller.app

    app = chess.controller.app.App()
    app.main_menu.execute()
