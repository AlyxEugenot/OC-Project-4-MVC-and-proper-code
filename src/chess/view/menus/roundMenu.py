import chess.model
import chess.view
import chess.view.menus
import chess.view.menus._abstract as _abstract


class RoundHandling(_abstract.Menu):
    def __init__(self):
        self.round: chess.model.Round = None
        super().__init__(title="Round vide")
        self.loop_above = True

        # self.matches =

        self.callback_get_round_from_id = _abstract.not_implemented
        self.callback_start_round = _abstract.not_implemented
        self.callback_end_round = _abstract.not_implemented
        self.callback_start_new_round = _abstract.not_implemented

    def on_exit(self):
        self.round = None
        self.context.current_round_id = None
        self.title = f"Round vide"

    def load_round(self):  # TODO va falloir appeler cette fonction quelque part :>
        if self.context.current_round_id is None:
            raise TypeError("Trying to load a round it does not find.")
        self.round = chess.model.Round.from_id(self.context.current_round_id)
        self.title = f"Round {str(self.round)}"

    def execute(self):
        while True:
            if self.round is None:
                raise RuntimeError("Round should be set.")

            self.children.clear()

            if self.round.end_time is not None:
                pass  # TODO ?
            elif not self.any_match_not_over():
                self.add_child(
                    _abstract.Action(
                        "Commencer un nouveau round.", self.start_new_round
                    )
                )
            else:
                # créer une copie de la liste
                matches = list(self.round.matches)
                unfinished_matches = [x for x in matches if not x.is_over()]
                for match in unfinished_matches:
                    self.add_child(
                        _abstract.Action(  # FIXME pas une action si "match" est un menu
                            f"En cours: {match.players[0]} vs {match.players[1]}",
                        )
                    )
                    matches.remove(match)
                for r in matches:
                    # self.add_child(RoundHandling(unfinished_round)) # TODO round handling
                    # ou peut-être juste un print des rounds terminés
                    self.add_child(_abstract.Action(f"Terminé: {str(r)}"))

            super().execute()

    def start_round(self):
        self.callback_start_round()
        self.start_new_round()

    def play_match(match: chess.model.Match):
        # passer dans un autre menu ?
        pass

    def end_round(self):
        self.callback_end_round()

    def start_new_round(self):
        self.callback_start_new_round()

    def any_match_not_over(self) -> bool:
        for match in self.round.matches:
            if not match.is_over():
                return True
        return False
