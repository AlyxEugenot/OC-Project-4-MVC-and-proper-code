"""Menu for reports display.

Reports:
    all_players,
    all_tournaments,
    all_players_from_tournament,
    rounds_matches_from_tournament,
    rounds_from_tournament,
    matches_from_tournament
"""

import tabulate
from chess.controller.menus import _abstract


class Reports(_abstract.Menu):
    """Menu for reports display.

    Inherit from Menu.

    Parent of actions:
        all_players
        all_tournaments
        all_players_from_tournament
        all_rounds_of_tournament_and_all_their_matches
        all_rounds_of_tournament
        all_matches_of_round
    """

    def __init__(self):
        """Initialize super init and set all callbacks.

        Add children:
            all_players
            all_tournaments
            all_players_from_tournament
            all_rounds_of_tournament_and_all_their_matches
            all_rounds_of_tournament
            all_matches_of_round
        """
        title = "Rapports"
        menu_option_name = "Afficher les rapports"
        super().__init__(title=title, menu_option_name=menu_option_name)

        # tabulate.PRESERVE_WHITESPACE = True  # marche pô ?
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

    def all_players(self, print_from_reports: bool = True) -> str:
        """Report all players.

        Columns are:
            ID
            Last name
            First name
            Birth date
            Elo

        Args:
            print_from_reports (bool, optional): Display from menu Reports if
                True. Defaults to True.

        Returns:
            str: str table to print.
        """
        all_players_list = self.callback_all_players()

        return self.display_by_table(
            all_players_list, print_from_function=print_from_reports
        )

    def all_tournaments(self, print_from_reports: bool = True) -> str:
        """Report all tournaments.

        Columns are:
            ID
            Tournament name
            Players and scores
            Rounds
            Address
            Round amount
            Description
            Tournament beginning datetime
            Tournament ending datetime

        Args:
            print_from_reports (bool, optional): Display from menu Reports if
                True. Defaults to True.

        Returns:
            str: str table to print.
        """
        tournaments_list = self.callback_all_tournaments()
        return self.display_by_table(
            tournaments_list,
            is_multiline=True,
            print_from_function=print_from_reports,
        )

    def all_players_from_tournament(
        self, tournament_id: str | int = None, print_from_reports: bool = True
    ) -> str:
        """Report all players from a tournament.

        Columns are:
            ID
            Last name
            First name
            Birth date
            Elo

        Args:
            tournament_id (str | int, optional): Tournament to show players
                from. Get input of which tournament if None. Defaults to None.
            print_from_reports (bool, optional): Display from menu Reports if
                True. Defaults to True.

        Returns:
            str: str table to print.
        """
        if tournament_id is None:
            tournament_id = self.view.my_input("ID du tournoi : ")
        # pylint: disable=assignment-from-no-return
        players_list = self.callback_all_players_from_tournament(
            str(tournament_id)
        )
        return self.display_by_table(
            players_list, print_from_function=print_from_reports
        )

    def all_rounds_of_tournament_and_all_their_matches(
        self, tournament_id: str | int = None, print_from_reports: bool = True
    ) -> str:
        """Report all rounds and matches from tournament.

        Columns are:
            ID
            Round name
            Matches (format player1[W]: 1, player2: 0)
            Round beginning datetime
            Round ending datetime

        Args:
            tournament_id (str | int, optional): Tournament to show rounds and
                matches from. Get input of which tournament if None.
                Defaults to None.
            print_from_reports (bool, optional): Display from menu Reports if
                True. Defaults to True.

        Returns:
            str: str table to print.
        """
        if tournament_id is None:
            tournament_id = self.view.my_input("ID du tournoi : ")
        # pylint: disable=assignment-from-no-return
        rounds_list = self.callback_rounds_matches_from_tournament(
            str(tournament_id)
        )
        return self.display_by_table(
            rounds_list,
            is_multiline=True,
            table_col_width_if_multiline=29,
            print_from_function=print_from_reports,
        )

    def all_rounds_of_tournament(
        self, tournament_id: str | int = None, print_from_reports: bool = True
    ) -> str:
        """Report all rounds from tournament.

        Columns are:
            ID
            Round name
            Match IDs
            Round beginning datetime
            Round ending datetime

        Args:
            tournament_id (str | int, optional): Tournament to show rounds
                from. Get input of which tournament if None. Defaults to None.
            print_from_reports (bool, optional): Display from menu Reports if
                True. Defaults to True.

        Returns:
            str: str table to print.
        """
        if tournament_id is None:
            tournament_id = self.view.my_input("ID du tournoi : ")
        # pylint: disable=assignment-from-no-return
        rounds_list = self.callback_rounds_from_tournament(str(tournament_id))
        return self.display_by_table(
            rounds_list, print_from_function=print_from_reports
        )

    def all_matches_of_round(
        self, round_id: str | int = None, print_from_reports: bool = True
    ) -> str:
        """Report all matches from round.

        Columns are:
            ID
            Players and scores
            White player

        Args:
            round_id (str | int, optional): Round to show matches from.
                Get input of which round if None. Defaults to None.
            print_from_reports (bool, optional): Display from menu Reports if
                True. Defaults to True.

        Returns:
            str: str table to print.
        """
        if round_id is None:
            round_id = self.view.my_input("ID du round : ")
        # pylint: disable=assignment-from-no-return
        matches_list = self.callback_matches_from_tournament(str(round_id))
        return self.display_by_table(
            matches_list, print_from_function=print_from_reports
        )

    def display_by_table(
        self,
        results_to_display: list[list[str]],
        is_multiline: bool = False,
        table_col_width_if_multiline: int = 11,
        print_from_function: bool = True,
    ) -> str:
        """Display nested list results as str table.

        Style is rounded_outline if table is multiline and fancy_grid is not.

        Args:
            results_to_display (list[list[str]]): Nested list to display.
                First row is headers.
            is_multiline (bool, optional): True if one of the columns is
                multiline. Defaults to False.
            table_col_width_if_multiline (int, optional): Max column width
                when table is multiline. Defaults to 11.
            print_from_function (bool, optional)): Prints from the function by
                default.

        Returns:
            str: str table to print.
        """
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

        if print_from_function:
            self.view.my_print(table)

        return table


if __name__ == "__main__":
    # pylint: disable=unnecessary-lambda
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
