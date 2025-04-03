import chess.model
import chess.controller.menus as menus
import chess.controller.context
import chess.model.callbacks


class App:
    def __init__(self):
        self.context = chess.controller.context.Context()
        self.main_menu = menus.MainMenu(self.context)

        self.setup_view()

    def setup_view(self):
        tournament = self.main_menu.tournament
        tournament.callback_add_players_to_tournament = (
            chess.model.callbacks.add_player_to_tournament
        )
        tournament.callback_start_new_round = chess.model.callbacks.start_new_round
        round_menu = tournament.round_menu
        match_menu = round_menu.match_menu
        match_menu.context = round_menu.context = self.context
        round_menu.callback_update_tournament_scores = (
            chess.model.callbacks.update_tournament_scores
        )

        reports = menus._abstract.find_menu(menus.Reports, self.main_menu)
        reports.callback_all_players = chess.model.callbacks.list_players
        reports.callback_all_tournaments = chess.model.callbacks.list_tournaments
        reports.callback_all_players_from_tournament = (
            lambda id: chess.model.callbacks.list_players_from_tournament(id)
        )
        reports.callback_rounds_from_tournament = (
            lambda id: chess.model.callbacks.list_rounds_from_tournament(id)
        )
        reports.callback_rounds_matches_from_tournament = (
            lambda id: chess.model.callbacks.list_rounds_from_tournament(
                id, match_is_int=False
            )
        )
        reports.callback_matches_from_tournament = (
            lambda id: chess.model.callbacks.list_matches_from_round(id)
        )


if __name__ == "__main__":
    app = App()
    app.main_menu.execute()
