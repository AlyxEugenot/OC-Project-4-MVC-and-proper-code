import chess.view
import chess.view.menus
import chess.view.menus._abstract as _abstract
import chess.model.generate as generate

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
import chess.model as model



class RoundHandling(_abstract.Menu):
    def __init__(self):
        self.round: model.Round = None
        # self.rounds=None
        super().__init__(title="Round vide")
        self.loop_above = True

        self.callback_get_round_from_id = _abstract.not_implemented
        self.callback_start_round = _abstract.not_implemented
        self.callback_end_round = _abstract.not_implemented
        self.callback_start_new_round = _abstract.not_implemented
        self.callback_any_match_not_over = _abstract.not_implemented

    def on_exit(self):
        self.round = None
        self.context.current_round_id = None
        self.title = f"Round vide"

    def load_round(self):  # TODO va falloir appeler cette fonction quelque part :>
        if self.context.current_round_id is None:
            raise TypeError("Trying to load a round it does not find.")
        self.round = self.callback_get_round_from_id(
            self.context.current_round_id
        )
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
                matches = self.round.matches
                unfinished_matches = [x for x in matches if x.end_time is not None]
                if len(unfinished_matches) > 1:
                    raise RecursionError(
                        "Multiple unfinished rounds. Normally impossible."
                    )
                unfinished_matches = unfinished_matches[0]
                # self.add_child(RoundHandling(unfinished_round)) # TODO round handling
                self.add_child(
                    _abstract.Action(
                        f"En cours: {unfinished_matches.name}",
                    )
                )
                matches.remove(unfinished_matches[0])
                for r in matches:
                    # self.add_child(RoundHandling(unfinished_round)) # TODO round handling
                    # ou peut-être juste un print des rounds terminés
                    self.add_child(_abstract.Action(f"Terminé: {r.name}"))

            super().execute()

    def start_round(self):
        self.callback_start_round()
        self.start_new_round()

    def end_round(self):
        self.callback_end_round()

    def start_new_round(self):
        self.callback_start_new_round()

    def any_match_not_over(self) -> bool:
        return self.callback_any_match_not_over(self.context.current_tournament_id)

