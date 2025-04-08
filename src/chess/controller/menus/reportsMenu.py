import chess.controller.menus._abstract as _abstract
import tabulate


class Reports(_abstract.Menu):
    def __init__(self):
        title = "Rapports"
        menu_option_name = "Afficher les rapports"
        super().__init__(title=title, menu_option_name=menu_option_name)

        tabulate.PRESERVE_WHITESPACE = True  # marche pô ?
        self.callback_all_players = _abstract.not_implemented
        self.callback_all_tournaments = _abstract.not_implemented
        self.callback_all_players_from_tournament = _abstract.not_implemented
        self.callback_rounds_matches_from_tournament = (
            _abstract.not_implemented
        )
        self.callback_rounds_from_tournament = _abstract.not_implemented
        self.callback_matches_from_tournament = _abstract.not_implemented

        self.add_child(
            _abstract.Action("Liste de tous les joueurs", self.all_players)
        )
        self.add_child(
            _abstract.Action(
                "Liste de tous les tournois", self.all_tournaments
            )
        )
        self.add_child(
            _abstract.Action(
                "Liste de tous les joueurs d'un tournoi",
                self.all_players_from_tournament,
            )
        )
        self.add_child(
            _abstract.Action(
                "Liste de tous les rounds d'un tournoi et tous ses matchs",
                self.all_rounds_of_tournament_and_all_their_matches,
            )
        )
        self.add_child(
            _abstract.Action(
                "Liste de tous les rounds d'un tournoi",
                self.all_rounds_of_tournament,
            )
        )
        self.add_child(
            _abstract.Action(
                "Liste de tous les matchs d'un round",
                self.all_matches_of_round,
            )
        )

    def all_players(self):
        all_players_list = self.callback_all_players()
        Reports.display_by_table(all_players_list)

    def all_tournaments(self):
        tournaments_list = self.callback_all_tournaments()
        Reports.display_by_table(tournaments_list, is_multiline=True)

    def all_players_from_tournament(self, tournament_id: str = None):
        if tournament_id is None:
            tournament_id = self.view.my_input("ID du tournoi : ")
        players_list = self.callback_all_players_from_tournament(tournament_id)
        Reports.display_by_table(players_list)

    def all_rounds_of_tournament_and_all_their_matches(
        self, tournament_id: str = None
    ):
        if tournament_id is None:
            tournament_id = self.view.my_input("ID du tournoi : ")
        rounds_list = self.callback_rounds_matches_from_tournament(
            tournament_id
        )
        Reports.display_by_table(
            rounds_list, is_multiline=True, table_col_width_if_multiline=29
        )

    def all_rounds_of_tournament(self, tournament_id: str = None):
        if tournament_id is None:
            tournament_id = self.view.my_input("ID du tournoi : ")
        rounds_list = self.callback_rounds_from_tournament(tournament_id)
        Reports.display_by_table(rounds_list)

    def all_matches_of_round(self, round_id: str = None):
        if round_id is None:
            round_id = self.view.my_input("ID du round : ")
        matches_list = self.callback_matches_from_tournament(round_id)
        Reports.display_by_table(matches_list)

    def display_by_table(
        self,
        results_to_display: list[list[str]],
        is_multiline: bool = False,
        table_col_width_if_multiline: int = 11,
    ) -> str:
        if is_multiline:
            table = tabulate.tabulate(
                results_to_display,
                headers="firstrow",
                tablefmt="fancy_grid",
                maxcolwidths=table_col_width_if_multiline,
                maxheadercolwidths=table_col_width_if_multiline,
            )
        else:
            table = tabulate.tabulate(
                results_to_display,
                headers="firstrow",
                tablefmt="rounded_outline",
                stralign="center",
            )

        self.view.my_print(table)


if __name__ == "__main__":
    import chess.model.callbacks

    reports = Reports()
    reports.callback_all_players = chess.model.callbacks.report_players
    reports.callback_all_tournaments = chess.model.callbacks.report_tournaments
    reports.callback_all_players_from_tournament = (
        lambda id: chess.model.callbacks.report_players_from_tournament(id)
    )
    reports.callback_all_tournaments = chess.model.callbacks.report_tournaments
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

    # reports.all_players()
    # reports.all_tournaments()
    # reports.all_players_from_tournament()
    reports.all_rounds_of_tournament_and_all_their_matches()
