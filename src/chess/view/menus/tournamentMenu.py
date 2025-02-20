import chess.view
import chess.view.menus._abstract as _abstract
import chess.model as model
import chess.model.generate as generate


class WhichTournament(_abstract.Menu):
    def __init__(self):
        title = "Choisir un tournoi"
        menu_option_name = "Tournoi"
        super().__init__(menu_option_name=menu_option_name, title=title)

        self.add_tournaments_to_continue()
        self.add_child(_abstract.Action("Créer un tournoi", self.create_tournament))

    def add_tournaments_to_continue(self):
        tournaments_ids = model.load_data()[model.storage.TOURNAMENTS].keys()
        all_tournaments = [model.tournament_from_id(x) for x in tournaments_ids]
        unfinished_tournaments = [x for x in all_tournaments if x.end_time is None]
        for t in unfinished_tournaments:
            self.add_child(TournamentHandling(t))

    def create_tournament(self) -> model.Tournament:
        tournament_id = input("Quel est l'ID du tournoi ? (generate random if empty) ")

        if model.storage.tournament_from_id(tournament_id) is not None:
            # TODO confirmation de "on a trouvé un tournoi à tel ID, voulez-vous en créer un avec un ID différent ?"
            return model.storage.tournament_from_id(tournament_id)

        if generate.is_empty_string(tournament_id):
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
    def __init__(self, tournament: model.Tournament):
        menu_option_name = str(tournament)
        title = "Tournoi"
        self.tournament = tournament
        super().__init__(menu_option_name, title)
        self.loop_above = True

        # self.parent = self.parent.parent #FIXME l'héritage n'est pas encore initialisé

    def execute(self):
        while True:
            if type(self.parent) is WhichTournament:
                self.parent = self.parent.parent

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
                    _abstract.Action("Commencer un nouveau round.", self.start_new_round)
                )
            else:
                rounds = self.tournament.rounds
                unfinished_round = [x for x in rounds if x.end_time is not None]
                if len(unfinished_round) > 1:
                    raise RecursionError("Multiple unfinished rounds. Normally impossible.")
                unfinished_round = unfinished_round[0]
                # self.add_child(RoundHandling(unfinished_round)) # TODO round handling
                self.add_child(_abstract.Action(f"En cours: {unfinished_round.name}"))
                rounds.remove(unfinished_round[0])
                for r in rounds:
                    # self.add_child(RoundHandling(unfinished_round)) # TODO round handling
                    # ou peut-être juste un print des rounds terminés
                    self.add_child(_abstract.Action(f"Terminé: {r.name}"))

            super().execute()

    def start_tournament(self):
        print("start")
        self.start_new_round()

    def end_tournament(self):
        print("end")

    def start_new_round(self):
        print("start new round")

    def add_players_to_tournament(self):
        print("add_players")

    def add_rounds_to_menu(self):
        print("add_rounds")

    def any_round_not_over(self) -> bool:
        return True  # TODO change from view to model
        # mettre callback en paramètre
