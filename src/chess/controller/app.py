"""Main controller. Entry point to the program after chessTournamentApp."""

from chess.controller import menus, context
from chess.model import callbacks
from chess.view import View


class App:
    """Main Controller.

    Set up the program. Initiate menus. Set up callbacks, context, view.
    """

    def __init__(self):
        """Set up the program.

        Initiate menus. Set up callbacks, context, view.
        """
        self.context = context.Context()
        self.view = View()
        self.main_menu = menus.MainMenu(self.context, self.view)
        self.view.my_print_header()

        self.setup()

    def setup(self):
        """Set up menu and reports callbacks."""
        self.setup_permanent_menus()
        self.setup_reports()
        self.setup_view()

        self.context.current_menu = self.main_menu

    def setup_permanent_menus(self):
        """Set up menu callbacks."""
        tournament_menu: menus.TournamentHandling = (
            self.main_menu.tournament_menu
        )
        tournament_menu.callback_add_players_to_tournament = (
            callbacks.add_player_to_tournament
        )
        tournament_menu.callback_start_new_round = callbacks.start_new_round
        round_menu: menus.RoundHandling = tournament_menu.round_menu
        round_menu.callback_update_tournament_scores = (
            callbacks.update_tournament_scores
        )

    def setup_reports(self):
        """Set up reports callbacks."""
        # pylint: disable=protected-access, unnecessary-lambda
        reports: menus.Reports = menus._abstract.find_menu(
            menus.Reports, self.main_menu
        )
        reports.callback_all_players = callbacks.report_players
        reports.callback_all_tournaments = callbacks.report_tournaments
        reports.callback_all_players_from_tournament = (
            lambda id: callbacks.report_players_from_tournament(id)
        )
        reports.callback_rounds_from_tournament = (
            lambda id: callbacks.report_rounds_from_tournament(id)
        )
        reports.callback_rounds_matches_from_tournament = (
            lambda id: callbacks.report_rounds_from_tournament(
                id, match_is_int=False
            )
        )
        reports.callback_matches_from_tournament = (
            lambda id: callbacks.report_matches_from_round(id)
        )

    def setup_view(self):
        """Setup view callbacks for regular inputs."""
        self.view.callback_input_cancel = lambda: callbacks.cancel(
            current_menu=self.context.current_menu,
            current_menu_arborescence=self.view.current_menu_arborescence,
            my_print=self.view.my_print,
            menu_header=self.view.my_print_header,
        )
        self.view.callback_input_main_menu = (
            lambda: callbacks.execute_main_menu(
                main_menu=self.main_menu,
                current_menu_arborescence=self.view.current_menu_arborescence,
                menu_header=self.view.my_print_header,
            )
        )
        self.view.callback_input_quit = lambda: callbacks.quit_program(
            self.view.my_print
        )


if __name__ == "__main__":
    app = App()
    app.main_menu.execute()
