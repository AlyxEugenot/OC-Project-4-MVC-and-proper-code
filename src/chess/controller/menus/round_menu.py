"""Menu handling rounds.

Raises:
    TypeError: TypeError raised if round ID was not found when loaded.
    RuntimeError: RuntimeError raised if function body is run when round\
        ID not found.
"""

import chess.model
import chess.controller.menus
from chess.controller.menus import _abstract


class RoundHandling(_abstract.Menu):
    """Menu handling rounds.

    Inherit from Menu.

    Children:
        end_round (Action)
        load_match (Action)

    Parent of MatchHandling (Menu)
    """

    def __init__(self):
        """Initialize super init. Set update_tournament_scores callback.

        Add children:
            end_round
            load_match

        Set as parent to MatchHandling.
        """
        self.round: chess.model.Round = None
        super().__init__(title="Round vide")
        self.loop_above = True

        # set up round-match parent relationship
        self.match_menu: chess.controller.menus.MatchHandling = (
            self.add_remanent_menu_not_child(
                chess.controller.menus.MatchHandling()
            )
        )

        self.callback_update_tournament_scores = _abstract.not_implemented

    def on_exit(self):
        """Reset RoundHandling when exiting menu back to TournamentHandling."""
        self.parent.load_tournament()
        self.round = None
        self.context.current_round_id = None
        self.title = "Round vide"
        super().on_exit()

    def load_round(self):
        """When entering this round, get id from context and enable menu.

        Raises:
            TypeError: TypeError raised if round_id is None in context.
        """
        if self.context.current_round_id is None:
            raise TypeError("Trying to load a round it does not find.")
        self.round = chess.model.Round.from_id(self.context.current_round_id)
        self.title = str(self.round)
        self.view.my_print("Chargement du round...")
        self._update_current_menu(self)

    def execute(self):
        """Navigate to different matches.

        Raises:
            RuntimeError: RuntimeError raised if round not loaded.
        """
        while True:
            if self.round is None:
                raise RuntimeError("Round should be set.")

            self.children.clear()

            if self.round.end_time is not None:
                self.add_child(
                    _abstract.Action(
                        "Rapport : afficher les rounds terminés de ce tour.",
                        lambda: self.display_report(
                            self.reports.all_matches_of_round,
                            str(self.context.current_round_id),
                        ),
                    )
                )
                super().execute()
                continue
                # on ne veut pas pouvoir modifier les matchs déjà finis dans un
                # round passé donc on fait pas la suite de la while loop
            if not self.any_match_not_over():
                self.add_child(
                    _abstract.Action(
                        "Terminer le round et revenir au tournoi.",
                        lambda: self.end_round(start_new_round=False),
                    )
                )
                if not self.parent.tournament_final_round_reached():
                    self.add_child(
                        _abstract.Action(
                            "Terminer le round et commencer le nouveau.",
                            self.end_round,
                        )
                    )

            # créer une copie de la liste
            matches: list[chess.model.Match] = list(self.round.matches)
            unfinished_matches = [x for x in matches if not x.is_over()]
            for match in unfinished_matches:
                self.add_child(
                    _abstract.Action(
                        f"En cours: {match.players[0]} vs {match.players[1]}",
                        lambda id=match.id: self.load_match(id),
                    )
                )
                matches.remove(match)
            for match in matches:
                self.add_child(
                    _abstract.Action(
                        f"Terminé: {str(match)}",
                        lambda id=match.id: self.load_match(id),
                    )
                )

            self.add_child(
                _abstract.Action(
                    "Rapport : afficher les matchs de ce tour.",
                    lambda: self.display_report(
                        self.reports.all_matches_of_round,
                        str(self.context.current_round_id),
                    ),
                )
            )

            super().execute()

    def load_match(self, match_id: int):
        """Load match. Then execute MatchHandling menu.

        Args:
            match_id (int): ID of match to load.
        """
        self.context.current_match_id = match_id
        self.match_menu.load_match()
        self.match_menu.execute()

    def end_round(self, start_new_round: bool = True):
        """End and exit round. Set end_time to round.

        Start new round instantly if start_new_round is True instead of
        going back to TournamentHandling.

        Args:
            start_new_round (bool, optional): Start new round instead of
                going back to TournamentHandling if True. Defaults to True.
        """
        self.round.end_round()
        self.callback_update_tournament_scores(
            self.parent.tournament, self.round.matches
        )
        if start_new_round:
            self.parent.start_new_round()
        else:
            self.parent.load_tournament()
            self.parent.execute()

    def any_match_not_over(self) -> bool:
        """True if any match is unresolved.

        Returns:
            bool: True if any match is unresolved.
        """
        for match in self.round.matches:
            if not match.is_over():
                return True
        return False
