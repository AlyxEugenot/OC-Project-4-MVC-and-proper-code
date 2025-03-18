import chess.model
import chess.view
import chess.view.menus
import chess.view.menus._abstract as _abstract
import chess.view.menus.matchMenu


class RoundHandling(_abstract.Menu):
    def __init__(self):
        self.round: chess.model.Round = None
        super().__init__(title="Round vide")
        self.loop_above = True

        self.match_menu = chess.view.menus.matchMenu.MatchHandling()
        # set up round-match parent relationship
        self.add_child(self.match_menu)
        self.children.remove(self.match_menu)
        
        self.callback_update_tournament_scores=_abstract.not_implemented

    def on_exit(self):
        self.parent.load_tournament()
        self.round = None
        self.context.current_round_id = None
        self.title = f"Round vide"

    def load_round(self):  # TODO va falloir appeler cette fonction quelque part :>
        if self.context.current_round_id is None:
            raise TypeError("Trying to load a round it does not find.")
        self.round = chess.model.Round.from_id(self.context.current_round_id)
        self.title = str(self.round)

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
                        "Terminer le round et commencer le prochain.",
                        self.end_round,
                    )
                )
            else:
                # créer une copie de la liste
                matches = list(self.round.matches)
                unfinished_matches = [x for x in matches if not x.is_over()]
                for match in unfinished_matches:
                    self.add_child(
                        _abstract.Action(
                            f"En cours: {match.players[0]} vs {match.players[1]}",  # str pour prénom nom ?
                            lambda id=match.id: self.load_match(id),
                        )
                    )
                    matches.remove(match)
                for match in matches:
                    # self.add_child(RoundHandling(unfinished_round)) # TODO round handling
                    # ou peut-être juste un print des rounds terminés
                    self.add_child(
                        _abstract.Action(
                            f"Terminé: {str(match)}",
                            lambda id=match.id: self.load_match(id),
                        )
                    )

            super().execute()

    def load_match(self, match_id: int):
        self.context.current_match_id = match_id
        self.match_menu.load_match()
        self.match_menu.execute()

    def end_round(self):
        self.round.end_round()
        self.callback_update_tournament_scores(self.parent.tournament, self.round.matches)
        self.parent.load_tournament()
        self.parent.start_new_round()

    def any_match_not_over(self) -> bool:
        for match in self.round.matches:
            if not match.is_over():
                return True
        return False
