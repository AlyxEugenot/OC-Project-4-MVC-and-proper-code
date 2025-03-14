import datetime
from chess.model import Player, Address, Round
from typing import Self
from chess.model.storage import save_data, load_data, TOURNAMENTS, datetime_to_str




class Tournament:
    """Tournament class. Tournaments are split in multiple rounds."""

    def __init__(
        self,
        id: int,
        name: str,
        players: list[list[Player, int]],
        rounds: list[Round],
        localization: Address,
        rounds_amount: int = 4,
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
        description: str = "",
    ):  # FIXME redo docstring
        """Tournament init.

        Args:
            id (int): Tournament ID. Must be unique for saving/loading purposes.
            name (str): Tournament name.
            players (list[Player, int]): List of players and their points for\
                this tournament.
            localization (Address): Tournament address.
            rounds_amount (int, optional): Number of rounds until tournament's\
                end. Defaults to 4.
            description (str, optional): Tournament description.
        """
        self.id = id
        self.name = name
        self.players = [[player[0], player[1]] for player in players]
        self.rounds = rounds
        self.localization = localization
        self.rounds_amount = rounds_amount

        self.start_time = start_time
        self.end_time = end_time

        if description == "":
            self.description = (
                f"Tournament {name} at {localization.postcode}."
                # f"the {self.start_time}."
            )
        else:
            self.description = description

    def add_player(self, player: Player):
        self.players.append([player, 0])

    def start_tournament(self):
        self.start_time = datetime.datetime.now()
        self.save()

    def end_tournament(self):
        self.end_time = datetime.datetime.now()
        self.save()

    def save(self):
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
                    "players": [[player[0].id, player[1]] for player in self.players],
                    "rounds": [round.id for round in self.rounds],
                    "localization": self.localization.to_json(),
                    "rounds_amount": self.rounds_amount,
                    "description": self.description,
                    "start_time": datetime_to_str(self.start_time),
                    "end_time": datetime_to_str(self.end_time),
                }
            }
        }
        return this_json

    def from_id(tournament_id: int) -> Self:
        """Return Tournament object from json through id.
        Return None if ID not found.

        Args:
            tournament_id (int): Tournament ID

        Returns:
            Tournament: Tournament object
        """
        str_tournament_id = str(tournament_id)
        data = load_data()
        if TOURNAMENTS not in data:
            raise LookupError
        if str_tournament_id not in data[TOURNAMENTS]:
            return None
        json_ref = data[TOURNAMENTS][str_tournament_id]
        tournament = Tournament(
            id=tournament_id,
            name=json_ref["name"],
            players=[
                [Player.from_id(player[0]), player[1]] for player in json_ref["players"]
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

        return tournament

    def players_already_met(self, player1: Player, player2: Player) -> bool:
        for r in self.rounds:
            for m in r.matches:
                if player1 in m.players:
                    if player2 in m.players:
                        return True
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
