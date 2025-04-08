import chess.model
import chess.controller.menus._abstract as _abstract


class MatchHandling(_abstract.Menu):
    def __init__(self):
        self.match: chess.model.Match = None
        super().__init__(title="Match vide")
        self.loop_above = True

    def on_exit(self):
        self.parent.load_round()
        self.match = None
        self.context.current_match_id = None
        self.title = "Match vide"

    def load_match(self):
        if self.context.current_match_id is None:
            raise TypeError("Trying to load a match it does not find.")
        self.match = chess.model.Match.from_id(self.context.current_match_id)
        self.title = f"Match {str(self.match)}"

    def execute(self):
        while True:
            if self.match is None:
                raise RuntimeError("Match should be set.")

            self.children.clear()

            if self.match.is_over():
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
        self.match.declare_winner(player)
        self.on_exit()
        self.parent.execute()

    def reset_match(self):
        for player in self.match.score:
            self.match.score[player] = 0
        self.match.save()
