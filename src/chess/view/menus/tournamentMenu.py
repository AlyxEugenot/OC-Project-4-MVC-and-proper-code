import chess.view
import chess.view.menus
import chess.view.menus._abstract as _abstract
import chess.model.generate as generate

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
import chess.model as model
import chess.model.storage
import chess.view.menus.roundMenu


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
        tournaments_ids = chess.model.storage.load_data()[
            chess.model.storage.TOURNAMENTS
        ].keys()
        all_tournaments = [
            model.Tournament.from_id(int(x)) for x in tournaments_ids
        ]  # TODO enlever le int(x) quand j'aurai fait la fonction "envoie les id de tournois qui renverront que des int"
        unfinished_tournaments = [x for x in all_tournaments if x.end_time is None]
        for t in unfinished_tournaments:
            self.add_child(
                _abstract.Action(
                    f"Tournoi {t.name}", lambda id=t.id: self.select_tournament(id)
                )
            )

    def select_tournament(self, id: int):
        self.context.current_tournament_id = id
        self.parent.tournament.load_tournament()
        self.parent.tournament.execute()

    def create_tournament(self) -> model.Tournament:
        tournament_id = input("Quel est l'ID du tournoi ? (generate random if empty) ")

        if model.Tournament.from_id(tournament_id) is not None:
            # TODO confirmation de "on a trouvé un tournoi à tel ID, voulez-vous en créer un avec un ID différent ?"
            return model.Tournament.from_id(tournament_id)

        if tournament_id == "":
            tournament_id = generate.generate_available_id(
                chess.model.storage.TOURNAMENTS
            )
        name = input("Tournament name: ")
        players: str = input("Enter players' ID separated by commas:(can be empty) ")
        players = players.split(",")
        players_found = [
            player.strip()
            for player in players
            if model.Player.from_id(player.strip()) is not None
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
            rounds=[],
            localization=localization,
        )
        if rounds_amount != "":
            tournament.rounds_amount = int(rounds_amount)
        if description != "":
            tournament.description = description

        tournament.save()
        return tournament


class TournamentHandling(_abstract.Menu):
    def __init__(self):
        self.tournament: model.Tournament = None
        super().__init__(title="Tournoi vide")
        self.loop_above = True

        self.round_menu = chess.view.menus.roundMenu.RoundHandling()
        # set up tournament-round parent relationship
        self.add_child(self.round_menu)
        self.children.remove(self.round_menu)
        # créé pour récup les nombres de points des joueurs et bien commencer le nouveau round MAIS
        # inutile si on save à chaque fin de match et que l'on check les data à chaque fois qu'on veut connaitre les points
        # en plus, "le cumul des points" peut servir à pas mal d'endroits

        self.callback_start_new_round = _abstract.not_implemented  # done
        self.callback_add_players_to_tournament = _abstract.not_implemented  # done

    def on_exit(self):
        self.tournament = None
        self.context.current_tournament_id = None
        self.title = f"Tournoi vide"

    def load_tournament(self):
        if self.context.current_tournament_id is None:
            raise TypeError("Trying to load a tournament it does not find.")
        self.tournament = model.Tournament.from_id(self.context.current_tournament_id)
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
                if self.tournament_final_round_reached():
                    self.add_child(
                        _abstract.Action(
                            "Dernier round joué. Clôturer ce tournoi.",
                            self.end_tournament,
                        )
                    )
                else:
                    self.add_child(
                        _abstract.Action(
                            "Commencer un nouveau round.", self.start_new_round
                        )
                    )
            else:
                # créer une copie de la liste
                rounds = list(self.tournament.rounds)
                unfinished_round = [x for x in rounds if x.end_time is None]
                if len(unfinished_round) > 1:
                    raise RecursionError(
                        "Multiple unfinished rounds. Normally impossible."
                    )
                unfinished_round = unfinished_round[0]
                # self.add_child(RoundHandling(unfinished_round)) # TODO round handling
                self.add_child(
                    _abstract.Action(
                        f"En cours: {unfinished_round.name}",
                        lambda: self.load_round(unfinished_round.id),
                    )
                )
                rounds.remove(unfinished_round)
                for r in rounds:
                    # self.add_child(RoundHandling(unfinished_round)) # TODO round handling
                    # ou peut-être juste un print des rounds terminés
                    self.add_child(
                        _abstract.Action(
                            f"Terminé: {r.name}", lambda: self.load_round(r.id)
                        )
                    )

            super().execute()

    def start_tournament(self):
        self.tournament.start_tournament()
        self.start_new_round()

    def end_tournament(self):
        self.tournament.end_tournament()
        self.parent.execute()

    def start_new_round(self):
        round = self.callback_start_new_round(self.tournament)
        self.tournament.save()
        self.load_round(round.id)

    def load_round(self, round_id):
        self.context.current_round_id = round_id
        self.round_menu.load_round()
        self.round_menu.execute()

    def add_players_to_tournament(self):
        # afficher les joueurs ajoutables au tournoi
        while True:
            id = input("ID du joueur: ")
            if id == "":
                break

            result = self.callback_add_players_to_tournament(id, self.tournament)
            if result is None:
                print("Joueur non trouvé. Ne rien entrer pour revenir au tournoi.\n")
            else:
                print("Joueur ajouté. Ne rien entrer pour revenir au tournoi.\n")

    def any_round_not_over(self) -> bool:
        for round in self.tournament.rounds:
            if round.end_time is None:
                return True
        return False

    def tournament_final_round_reached(self) -> bool:
        if len(self.tournament.rounds) >= self.tournament.rounds_amount:
            return True
        else:
            return False
