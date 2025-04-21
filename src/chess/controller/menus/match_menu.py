"""Menu handling matches.

Raises:
    TypeError: TypeError raised if match ID was not found when loaded.
    RuntimeError: RuntimeError raised if function body is run when match\
        ID not found.
"""

import chess.model
from chess.controller.menus import _abstract


class MatchHandling(_abstract.Menu):
    """Menu handling matches.

    Inherit from Menu.

    Children:
        declare_winner (Action)
        reset_match (Action)
    """

    def __init__(self):
        """Initialize super init.

        Children:
            declare winner
            reset_match
        """
        self.match: chess.model.Match = None
        super().__init__(title="Match vide")
        self.loop_above = True

    def on_exit(self):
        """Reset MatchHandling when exiting menu back to RoundHandling."""
        self.parent.load_round()
        self.match = None
        self.context.current_match_id = None
        self.title = "Match vide"
        super().on_exit()

    def load_match(self):
        """When entering this menu, get id from context and enable menu.

        Raises:
            TypeError: TypeError raised if match_id is None in context.
        """
        if self.context.current_match_id is None:
            raise TypeError("Trying to load a match it does not find.")
        self.match = chess.model.Match.from_id(self.context.current_match_id)
        self.title = f"Match {str(self.match)}"
        self.view.my_print("Chargement du match...")
        self._update_current_menu(self)

    def execute(self):
        """Declare winner of match. Match can be reset when finished.

        Raises:
            RuntimeError: RuntimeError raised if match not loaded.
        """
        while True:
            if self.match is None:
                raise RuntimeError("Match should be set.")

            self.children.clear()

            if self.match.is_over() and self.parent.round.end_time is None:
                self.add_child(
                    _abstract.Action(
                        f"{self.match.result()} Annuler le résultat ?",
                        self.reset_match,
                    )
                )
            else:
                self.add_child(
                    _abstract.Action(
                        f"Résultat: {self.match.players[0]} vainqueur.",
                        lambda: self.declare_winner(self.match.players[0]),
                    )
                )
                self.add_child(
                    _abstract.Action(
                        f"Résultat: {self.match.players[1]} vainqueur.",
                        lambda: self.declare_winner(self.match.players[1]),
                    )
                )
                self.add_child(
                    _abstract.Action(
                        "Résultat: égalité.",
                        lambda: self.declare_winner(None),
                    )
                )

            super().execute()

    def declare_winner(self, player: chess.model.Player | None):
        """Declare winner of the match. Tie if None.

        Args:
            player (chess.model.Player | None): Winning player. Tie if None.
        """
        self.match.declare_winner(player)
        self.on_exit()
        self.parent.execute()

    def reset_match(self):
        """Reset match to 0-0."""
        for player in self.match.score:
            self.match.score[player] = 0
        self.match.save()
