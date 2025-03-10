import chess.model.callbacks
import chess.view.menus
import chess.view.menus._abstract
import chess.view.menus.addPlayersMenu
import chess.view.menus.mainMenu
import chess.model

# import chess.controller.context

from typing import TYPE_CHECKING, Type

# if TYPE_CHECKING:
from chess.view.menus.roundMenu import RoundHandling
from chess.view.menus.addPlayersMenu import AddPlayers
from chess.view.menus.tournamentMenu import TournamentHandling, WhichTournament
from chess.view.menus.reportsMenu import WhichReports


class App:
    def __init__(self):
        self.context = Context()  # chess.controller.context.Context()
        self.view_main_menu = chess.view.menus.mainMenu.MainMenu(self.context)

        self.setup_view()

    def setup_view(self):
        tournament = self.view_main_menu.tournament
        tournament.callback_add_players_to_tournament = chess.model.callbacks.add_player_to_tournament
        # round = tournament.round

        reports = find_menu(WhichReports, self.view_main_menu)
        reports.callback_all_players=chess.model.callbacks.list_all_players


class Context:
    def __init__(self):
        self.current_tournament_id: int | None = None
        self.current_round_id: int | None = None
        self.current_match_id: int | None = None

    def __repr__(self):
        return (
            "IDs: "
            f"T:{self.current_tournament_id}|"
            f"R:{self.current_round_id}|"
            f"M:{self.current_match_id}"
        )


def find_menu(
    menutype: Type[chess.view.menus._abstract.Menu],
    menu_to_search: chess.view.menus._abstract.Menu,
) -> chess.view.menus._abstract.Menu | None:
    for child in menu_to_search.children:
        if issubclass(type(child), chess.view.menus._abstract.Menu):
            if type(child) is menutype:
                return child
            found_deeper = find_menu(menutype, child)
            if found_deeper is not None:
                return found_deeper


if __name__ == "__main__":
    app = App()
    app.view_main_menu.execute()
