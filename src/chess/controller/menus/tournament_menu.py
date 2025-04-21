"""Menu handling tournaments.

Raises:
    TypeError: TypeError raised if tournament ID was not found when loaded.
    RuntimeError: RuntimeError raised if function body is run when tournament\
        ID not found.
"""

from chess.controller.menus import _abstract, RoundHandling
from chess import model
from chess.model import generate, storage


class WhichTournament(_abstract.Menu):
    """Menu handling creation or loading of tournaments.

    Inherit from Menu.

    Children:
        select_tournament (Action)
        create_tournament (Action)
    """

    def __init__(self):
        """Initialize super init."""
        title = "Choisir un tournoi"
        menu_option_name = "Tournoi"
        super().__init__(title=title, menu_option_name=menu_option_name)
        self.loop_above = True

    def execute(self):
        """Show tournaments not finished yet.

        Show tournament creation.
        """
        while True:
            self.children.clear()

            self.add_tournaments_to_continue()
            self.add_child(
                _abstract.Action("Créer un tournoi", self.create_tournament)
            )

            return super().execute()

    def add_tournaments_to_continue(self):
        """Add to menu children all unfinished tournaments."""
        tournaments_ids = storage.load_data()[storage.TOURNAMENTS].keys()
        all_tournaments: list[model.Tournament] = [
            model.Tournament.from_id(int(x)) for x in tournaments_ids
        ]
        unfinished_tournaments = [
            x for x in all_tournaments if x.end_time is None
        ]
        for t in unfinished_tournaments:
            self.add_child(
                _abstract.Action(
                    f"Tournoi {t.name}",
                    lambda id=t.id: self.load_tournament(id),
                )
            )

    def load_tournament(self, _id: int):
        """Load tournament. Then execute TournamentHandling menu.

        Args:
            _id (int): ID of tournament to load.
        """
        self.context.current_tournament_id = _id
        self.parent.tournament.load_tournament()
        self.parent.tournament.execute()

    def create_tournament(self) -> model.Tournament:
        """Create tournament from user id. Can be generated if empty fields.

        Returns:
            model.Tournament: Created tournament.
        """
        tournament_id = self.input_tournament_id()
        name = self.view.my_input("Nom du tournoi: ")
        players: str = self.view.my_input(
            "Sélectionnez les ID de joueurs séparés par des "
            "virgules : (peut être vide) "
        )
        players = players.split(",")
        players_found = [
            player.strip()
            for player in players
            if model.Player.from_id(player.strip()) is not None
        ]
        localization_strs = self.view.create_adress("\nAdresse du tournoi: ")
        if localization_strs is None:
            localization = generate.generate_address(
                generate.generate_players(1)[0]
            )
        else:
            localization = model.Address(*localization_strs)
        rounds_amount = self.view.my_input("\nRounds amount (default 4): ")
        description = self.view.my_input("Description:(generate if empty) ")

        tournament = model.Tournament(
            _id=tournament_id,
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

    def input_tournament_id(self) -> int:
        """Get user to input available tournament id.

        Returns:
            int: Tournament ID.
        """
        tournament_id_is_ok = False
        problem = ""
        while not tournament_id_is_ok:
            if problem != "":
                self.view.my_print(f"\n{problem}\n")

            tournament_id = self.view.my_input(
                "Quel est l'ID du tournoi ? (Générer au hasard si vide) "
            )
            if tournament_id == "":
                tournament_id = generate.generate_available_id(
                    storage.TOURNAMENTS
                )
                break

            (tournament_id_is_ok, problem) = storage.is_id_valid(
                tournament_id, "tournaments"
            )
        return int(tournament_id)


class TournamentHandling(_abstract.Menu):
    """Menu handling tournaments.

    Inherit from Menu.

    Children:
        add_players_to_tournament (Action)
        start_tournament (Action)
        end_tournament (Action)
        start_new_round (Action)
        load_round (Action)

    Parent of RoundHandling (Menu)
    """

    def __init__(self):
        """Initialize super init.
        Set start_new_round and add_players_to_tournament callbacks.

        Add children:
            add_players_to_tournament
            start_tournament
            end_tournament
            start_new_round
            load_round

        Set as parent to RoundHandling.
        """
        self.tournament: model.Tournament = None
        super().__init__(title="Tournoi vide")
        self.loop_above = True

        # set up tournament-round parent relationship
        self.round_menu: RoundHandling = self.add_remanent_menu_not_child(
            RoundHandling()
        )

        self.callback_start_new_round = _abstract.not_implemented  # done
        self.callback_add_players_to_tournament = (
            _abstract.not_implemented
        )  # done

    def on_exit(self):
        """Reset TournamentHandling when exiting menu back to MainMenu."""
        self.tournament = None
        self.context.current_tournament_id = None
        self.title = "Tournoi vide"

    def load_tournament(self):
        """When entering this tournament, get id from context and enable menu.

        Raises:
            TypeError: TypeError raised if tournament_id is None in context.
        """
        if self.context.current_tournament_id is None:
            raise TypeError("Trying to load a tournament it does not find.")
        self.tournament = model.Tournament.from_id(
            self.context.current_tournament_id
        )
        self.title = f"Tournoi {str(self.tournament)}"

    def execute(self):
        """
        Handle Tournament:
            Add players if tournament not started.
            Create round if no current round.
            Navigate to round.
            End tournament if final round is played.

        Raises:
            RuntimeError: RuntimeError raised if tournament not loaded.
        """
        while True:
            if self.tournament is None:
                raise RuntimeError("Tournament should be set.")

            self.children.clear()

            if self.tournament.end_time is not None:
                pass
            # TODO reports résumé du tournoi (global à toutes les options ?)
            elif self.tournament.start_time is None:
                self.add_child(
                    _abstract.Action(
                        (
                            "Ajouter des joueurs au tournoi "
                            f"({len(self.tournament.players)} actuellement)."
                        ),
                        self.add_players_to_tournament,
                    )
                )
                if len(self.tournament.players) > 3:
                    self.add_child(
                        _abstract.Action(
                            "Commencer le tournoi.",
                            self.start_tournament,
                        )
                    )
                else:
                    self.view.my_print(
                        "Minimum 4 joueurs pour commencer le tournoi."
                    )
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
                self.add_child(
                    _abstract.Action(
                        f"En cours: {unfinished_round.name}",
                        lambda: self.load_round(unfinished_round.id),
                    )
                )
                rounds.remove(unfinished_round)
                for r in rounds:
                    self.add_child(
                        _abstract.Action(
                            f"Terminé: {r.name}", lambda: self.load_round(r.id)
                        )
                    )

            super().execute()

    def start_tournament(self):
        """Start tournament. Set start_time to tournament. Start new round."""
        self.tournament.start_tournament()
        self.start_new_round()

    def end_tournament(self):
        """End and exit tournament. Set end_time to tournament.

        Go back to main menu.
        """
        self.tournament.end_tournament()
        self.parent.execute()

    def start_new_round(self):
        """Create new round, load it and go to its menu."""
        # pylint: disable=assignment-from-no-return
        _round: model.Round = self.callback_start_new_round(self.tournament)
        self.tournament.save()
        self.load_round(_round.id)

    def load_round(self, round_id):
        """Load round. Then execute RoundHandling menu.

        Args:
            round_id (int): ID of round to load.
        """
        self.context.current_round_id = round_id
        self.round_menu.load_round()
        self.round_menu.execute()

    def add_players_to_tournament(self):
        """Let user input existing player IDs to add them to tournament."""
        # TODO afficher les joueurs ajoutables au tournoi
        while True:
            _id = self.view.my_input("ID du joueur: ")
            if _id == "":
                break

            # pylint: disable=assignment-from-no-return
            result = self.callback_add_players_to_tournament(
                _id, self.tournament
            )
            if result is None:
                self.view.my_print(
                    "Joueur non trouvé. "
                    "Ne rien entrer pour revenir au tournoi.\n"
                )
            else:
                self.view.my_print(
                    "Joueur ajouté. Ne rien entrer pour revenir au tournoi.\n"
                )

    def any_round_not_over(self) -> bool:
        """True if any round is not finished (no end_time).

        Returns:
            bool: True if any round is not finished.
        """
        for _round in self.tournament.rounds:
            if _round.end_time is None:
                return True
        return False

    def tournament_final_round_reached(self) -> bool:
        """True if number of rounds reached rounds_amount.

        Returns:
            bool: True if number of rounds reached rounds_amount.
        """
        if len(self.tournament.rounds) >= self.tournament.rounds_amount:
            return True
        return False
