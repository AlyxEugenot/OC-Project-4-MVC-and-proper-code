"""Main menu. Root of menu arborescence."""

from typing import TYPE_CHECKING
from chess.controller.menus import _abstract
from chess.controller.menus import tournamentMenu
from chess.controller.menus import addPlayersMenu
from chess.controller.menus import reportsMenu


if TYPE_CHECKING:
    from chess.controller.context import Context
    from chess.view import View


class MainMenu(_abstract.Menu):
    """First menu the user interacts with.

    Inherit from Menu.

    Children:
        WhichTournament (Menu)
        AddPlayers (Menu)
        Reports (Menu)

    Parent of TournamentHandling (Menu)
    """

    def __init__(self, context: "Context", view: "View"):
        """Initialize super init.

        Set complete arborescence with late_init to set context and view.

        Add children:
            WhichTournament
            AddPlayers
            Reports

        Set as parent to TournamentHandling.

        Args:
            context (Context): Context object to share with all menus.
            view (View): View object to share with all menus.
        """
        title = "Menu principal"
        super().__init__(title=title)
        self.context = context
        self.view = view

        self.add_child(tournamentMenu.WhichTournament())
        self.add_child(addPlayersMenu.AddPlayers())
        self.add_child(reportsMenu.Reports())

        # set up tournament parent relationship
        self.tournament = self.invisible_child = (
            self.add_remanent_menu_not_child(
                tournamentMenu.TournamentHandling()
            )
        )

        self.late_init(am_root=True)


if __name__ == "__main__":
    import chess.controller.app

    app = chess.controller.app.App()
    app.main_menu.execute()
