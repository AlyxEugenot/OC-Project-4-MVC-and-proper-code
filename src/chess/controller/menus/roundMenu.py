import chess.model
import chess.controller.menus
import chess.controller.menus._abstract as _abstract


class RoundHandling(_abstract.Menu):
    def __init__(self):
        self.round: chess.model.Round = None
        super().__init__(title="Round vide")
        self.loop_above = True

        # set up round-match parent relationship
        self.match_menu = self.invisible_child = (
            self.add_remanent_menu_not_child(
                chess.controller.menus.MatchHandling()
            )
        )

        self.callback_update_tournament_scores = _abstract.not_implemented

    def on_exit(self):
        self.parent.load_tournament()
        self.round = None
        self.context.current_round_id = None
        self.title = "Round vide"

    def load_round(self):
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
                # TODO ?
                # rapport des matchs finis de ce round ?
                continue
                # on ne veut pas pouvoir modifier les matchs déjà finis dans un
                # round passé donc on fait pas la suite de la while loop
            elif not self.any_match_not_over():
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
            matches = list(self.round.matches)
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

            super().execute()

    def load_match(self, match_id: int):
        self.context.current_match_id = match_id
        self.match_menu.load_match()
        self.match_menu.execute()

    def end_round(self, start_new_round: bool = True):
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
        for match in self.round.matches:
            if not match.is_over():
                return True
        return False
