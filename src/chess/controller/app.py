import chess.model
import chess.controller.menus as menus
import chess.controller.context
import chess.model.callbacks
from chess.view import View


class App:
    def __init__(self):
        self.context = chess.controller.context.Context()
        self.view = View()
        self.main_menu = menus.MainMenu(self.context, self.view)

        self.setup()

    def setup(self):
        self.setup_permanent_menus()
        self.setup_reports()

    def setup_permanent_menus(self):
        tournament: menus.TournamentHandling = self.main_menu.tournament
        tournament.callback_add_players_to_tournament = (
            chess.model.callbacks.add_player_to_tournament
        )
        tournament.callback_start_new_round = chess.model.callbacks.start_new_round
        round_menu: menus.RoundHandling = tournament.round_menu
        round_menu.callback_update_tournament_scores = (
            chess.model.callbacks.update_tournament_scores
        )

    def setup_reports(self):
        reports: menus.Reports = menus._abstract.find_menu(
            menus.Reports, self.main_menu
        )
        reports.callback_all_players = chess.model.callbacks.report_players
        reports.callback_all_tournaments = chess.model.callbacks.report_tournaments
        reports.callback_all_players_from_tournament = (
            lambda id: chess.model.callbacks.report_players_from_tournament(id)
        )
        reports.callback_rounds_from_tournament = (
            lambda id: chess.model.callbacks.report_rounds_from_tournament(id)
        )
        reports.callback_rounds_matches_from_tournament = (
            lambda id: chess.model.callbacks.report_rounds_from_tournament(
                id, match_is_int=False
            )
        )
        reports.callback_matches_from_tournament = (
            lambda id: chess.model.callbacks.report_matches_from_round(id)
        )


if __name__ == "__main__":
    app = App()
    app.main_menu.execute()
