"""Tournament object."""

import datetime
from typing import Self
from chess.model import Player, Address, Round
from chess.model.storage import save_data, load_data, TOURNAMENTS
from chess import utils


class Tournament:
    """Tournament class. Tournaments are composed of multiple rounds."""

    def __init__(
        self,
        _id: int,
        name: str,
        players: list[list[Player, int]],
        rounds: list[Round],
        localization: Address,
        rounds_amount: int = 4,
        # start_time: datetime.datetime = None,
        # end_time: datetime.datetime = None,
        description: str = "",
    ):
        """Tournament init.

        Args:
            _id (int): Tournament ID. (len 6)
            name (str): Tournament name.
            players (list[list[Player, int]]): list of [Players, Scores] of
                tournament.
            rounds (list[Round]): All rounds from this tournament.
            localization (Address): Tournament address.
            rounds_amount (int, optional): Number of rounds until tournament
                end. Defaults to 4.
            description (str, optional): Tounament description. Defaults to
                "Tournoi {name} à {localization.postcode}."
        """
        self.id = _id
        self.name = name
        self.players = [[player[0], player[1]] for player in players]
        self.rounds = rounds
        self.localization = localization
        self.rounds_amount = rounds_amount

        self.start_time: datetime = None
        self.end_time: datetime = None

        if description == "":
            self.description = f"Tournoi {name} à {localization.postcode}."
        else:
            self.description = description

    def add_player(self, player: Player):
        """Add player to tournament.

        Args:
            player (Player): Player to add to tournament.
        """
        self.players.append([player, 0])

    def start_tournament(self):
        """Start tournament and set start_time."""
        self.start_time = datetime.datetime.now()
        self.save()

    def end_tournament(self):
        """End tournament and set end_time."""
        self.end_time = datetime.datetime.now()
        self.save()

    def save(self):
        """Save match in data.json."""
        save_data(self.to_json())

    def to_json(self) -> dict:
        """Return json implementation from Tournament object.

        Args:
            tournament (Tournament): Tournament object to save

        Returns:
            dict: json dict to use for saving
        """
        this_json = {
            TOURNAMENTS: {
                self.id: {
                    "name": self.name,
                    "players": [
                        [player[0].id, player[1]] for player in self.players
                    ],
                    "rounds": [round.id for round in self.rounds],
                    "localization": self.localization.to_json(),
                    "rounds_amount": self.rounds_amount,
                    "description": self.description,
                    "start_time": utils.datetime_to_isoformat(self.start_time),
                    "end_time": utils.datetime_to_isoformat(self.end_time),
                }
            }
        }
        return this_json

    # pylint: disable=no-self-argument
    def from_id(tournament_id: int) -> Self | None:
        """Return Tournament object from json through id.
        Return None if ID not found.

        Args:
            tournament_id (int): Tournament ID

        Returns:
            Tournament | None: Tournament object or None if not found.
        """
        str_tournament_id = str(tournament_id)
        data = load_data()
        if TOURNAMENTS not in data:
            raise LookupError
        if str_tournament_id not in data[TOURNAMENTS]:
            return None
        json_ref = data[TOURNAMENTS][str_tournament_id]
        tournament = Tournament(
            _id=tournament_id,
            name=json_ref["name"],
            players=[
                [Player.from_id(player[0]), player[1]]
                for player in json_ref["players"]
            ],
            rounds=[Round.from_id(id) for id in json_ref["rounds"]],
            localization=Address.from_json(json_ref["localization"]),
            rounds_amount=json_ref["rounds_amount"],
            description=json_ref["description"],
        )

        tournament.start_time = (
            datetime.datetime.fromisoformat(json_ref["start_time"])
            if json_ref["start_time"]
            else None
        )

        tournament.end_time = (
            datetime.datetime.fromisoformat(json_ref["end_time"])
            if json_ref["end_time"]
            else None
        )

        tournament.save()
        return tournament

    def players_already_met(self, player1: Player, player2: Player) -> bool:
        """Check if players met in previous rounds. Return True if so.

        Args:
            player1 (Player): Player to check if other player already played
                against.
            player2 (Player): Player to check if other player already played
                against.

        Returns:
            bool: True if players already met.
        """
        for r in self.rounds:
            for m in r.matches:
                ids = [player.id for player in m.players]
                if player1.id in ids:
                    if player2.id in ids:
                        return True
                    break  # plus d'équivalence possible dans ce round
        return False

    def __str__(self):
        """str method. Returns tournament's name.

        Returns:
            str: Tournament name.
        """
        return self.name

    def __repr__(self):
        """repr method. Returns tournament's ID.

        Returns:
            int: Tournament ID.
        """
        return self.id
