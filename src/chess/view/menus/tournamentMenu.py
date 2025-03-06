import chess.view
import chess.view.menus._abstract as _abstract
import chess.model.generate as generate

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
import chess.model as model


class WhichTournament(_abstract.Menu):
    def __init__(self):
        title = "Choisir un tournoi"
        menu_option_name = "Tournoi"
        super().__init__(title=title, menu_option_name=menu_option_name)
        self.loop_above = True

    def execute(self):
        while True:
            self.children.clear()

            self.add_tournaments_to_continue()
            self.add_child(_abstract.Action("Créer un tournoi", self.create_tournament))

            return super().execute()

    def add_tournaments_to_continue(self):
        tournaments_ids = model.load_data()[model.storage.TOURNAMENTS].keys()
        all_tournaments = [
            model.tournament_from_id(int(x)) for x in tournaments_ids
        ]  # TODO enlever le int(x) quand j'aurai fait la fonction "envoie les id de tournois qui renverront que des int"
        unfinished_tournaments = [x for x in all_tournaments if x.end_time is None]
        for t in unfinished_tournaments:
            self.add_child(
                _abstract.Action(
                    f"Tournoi {t.name}", lambda: self.select_tournament(t.id)
                )
            )

    def select_tournament(self, id: int):
        self.context.current_tournament_id = id
        self.parent.tournament.load_tournament()
        self.parent.tournament.execute()

    def create_tournament(self) -> model.Tournament:
        tournament_id = input("Quel est l'ID du tournoi ? (generate random if empty) ")

        if model.storage.tournament_from_id(tournament_id) is not None:
            # TODO confirmation de "on a trouvé un tournoi à tel ID, voulez-vous en créer un avec un ID différent ?"
            return model.storage.tournament_from_id(tournament_id)

        if tournament_id == "":
            tournament_id = generate.generate_specific_str("nnnnnn")
            while model.storage.tournament_from_id(tournament_id) is not None:
                tournament_id = generate.generate_specific_str("nnnnnn")
        name = input("Tournament name: ")
        players: str = input("Enter players' ID separated by commas:(can be empty) ")
        players = players.split(",")
        players_found = [
            player.strip()
            for player in players
            if model.storage.player_from_id(player.strip()) is not None
        ]
        localization = chess.view.create_address("\nTournament address: ")
        # TODO find avant
        # TODO faire le find address
        # TODO faire un menu pour les create address et player auquel au switch quand besoin ?
        rounds_amount = input("\nRounds amount (default 4): ")
        description = input("Description:(generate if empty) ")

        tournament = model.Tournament(
            id=tournament_id,
            name=name,
            players=players_found,
            localization=localization,
        )
        if rounds_amount != "":
            tournament.rounds_amount = int(rounds_amount)
        if description != "":
            tournament.description = description
        model.storage.save_data(model.storage.tournament_to_json(tournament))
        return tournament


class TournamentHandling(_abstract.Menu):
    def __init__(self):
        self.tournament = None
        super().__init__(title="Tournoi")
        self.loop_above = True

        self.callback_get_tournament_from_id = _abstract.not_implemented
        self.callback_start_tournament = _abstract.not_implemented
        self.callback_end_tournament = _abstract.not_implemented
        self.callback_start_new_round = _abstract.not_implemented
        self.callback_add_players_to_tournament = _abstract.not_implemented
        self.callback_add_rounds_to_menu = _abstract.not_implemented
        self.callback_any_round_not_over = _abstract.not_implemented

    def on_exit(self):
        self.tournament = None
        self.context.current_tournament_id = None
        self.title = f"Tournoi"

    def load_tournament(self):  # TODO va falloir appeler cette fonction quelque part :>
        if self.context.current_tournament_id is None:
            raise TypeError("Trying to load a tournament it does not find.")
        self.tournament = self.callback_get_tournament_from_id(
            self.context.current_tournament_id
        )
        self.title = f"Tournoi {str(self.tournament)}"

    def execute(self):
        while True:
            if self.tournament is None:
                raise RuntimeError("Tournament should be set.")

            self.children.clear()

            if self.tournament.end_time is not None:
                pass  # TODO ?
            elif self.tournament.start_time is None:
                self.add_child(
                    _abstract.Action(
                        f"Ajouter des joueurs au tournoi ({len(self.tournament.players)} actuellement).",
                        self.add_players_to_tournament,
                    )
                )
                if len(self.tournament.players) > 3:
                    self.add_child(
                        _abstract.Action(
                            f"Commencer le tournoi.",
                            self.start_tournament,
                        )
                    )
                else:
                    print("Minimum 4 joueurs pour commencer le tournoi.")
            elif not self.any_round_not_over():
                self.add_child(
                    _abstract.Action(
                        "Commencer un nouveau round.", self.start_new_round
                    )
                )
            else:
                rounds = self.tournament.rounds
                unfinished_round = [x for x in rounds if x.end_time is not None]
                if len(unfinished_round) > 1:
                    raise RecursionError(
                        "Multiple unfinished rounds. Normally impossible."
                    )
                unfinished_round = unfinished_round[0]
                # self.add_child(RoundHandling(unfinished_round)) # TODO round handling
                self.add_child(_abstract.Action(f"En cours: {unfinished_round.name}"))
                rounds.remove(unfinished_round[0])
                for r in rounds:
                    # self.add_child(RoundHandling(unfinished_round)) # TODO round handling
                    # ou peut-être juste un print des rounds terminés
                    self.add_child(_abstract.Action(f"Terminé: {r.name}"))

            super().execute()

    def get_tournament_from_data(self, tournament_id: int) -> model.Tournament | None:
        return self.callback_get_tournament_from_id(tournament_id)

    def start_tournament(self):
        self.callback_start_tournament()
        self.start_new_round()

    def end_tournament(self):
        self.callback_end_tournament()

    def start_new_round(self):
        self.callback_start_new_round()

    def add_players_to_tournament(self):
        # afficher les joueurs ajoutables au tournoi
        self.callback_add_players_to_tournament()

    def add_rounds_to_menu(self):
        self.callback_add_rounds_to_menu()

    def any_round_not_over(self) -> bool:
        return self.callback_any_round_not_over(self.context.current_tournament_id)
