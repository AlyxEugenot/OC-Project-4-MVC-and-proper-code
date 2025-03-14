import datetime
import random
from typing import Self, TYPE_CHECKING
from chess.model.storage import save_data, load_data, ROUNDS, datetime_to_str, MATCHES
from chess.model import Match


if TYPE_CHECKING:
    from chess.model import Tournament, Player


class Round:
    """Round class. Rounds are composed of multiple matches."""

    def __init__(
        self, id: int, name: str, matches: list[Match]
    ):  # , tournament: "Tournament"):
        """Round init.

        Args:
            id (int): Round ID. (len 6)
            name (str): Round Name. ex: "Round 1"
            matches(list[Match]): All matches of this round.


            tournament (Tournament): Tournament the round is a part of. #FIXME delete ?
        """
        self.id = id
        self.name = name
        # self.parent_tournament = tournament

        self.start_time = None
        self.end_time = None
        self.matches = matches

        self.start_round()
        self.save()

    def start_round(self):
        """Set the time for the round start.

        Returns:
            datetime.datetime: Datetime of beginning of round.
        """
        self.start_time = datetime.datetime.now()
        return self.start_time

    def end_round(self):
        """Set the time for the round end.

        Returns:
            datetime.datetime: Datetime of end of round.
        """
        self.end_time = datetime.datetime.now()
        return self.end_time

    def save(self):
        save_data(self.to_json())

    def to_json(self) -> dict:
        """Return json implementation from Round object.

        Args:
            round (Round): Round object to save

        Returns:
            dict: json dict to use for saving
        """
        this_json = {
            ROUNDS: {
                self.id: {
                    "name": self.name,
                    "matches": [match.id for match in self.matches],
                    # "parent_tournament": self.parent_tournament,
                    "start_time": datetime_to_str(self.start_time),
                    "end_time": datetime_to_str(self.end_time),
                }
            }
        }
        return this_json

    def from_id(round_id: int) -> Self:
        """Return Round object from json through id.
        Return None if ID not found.

        Args:
            round_id (int): Round ID

        Returns:
            Round: Round object
        """
        str_round_id = str(round_id)
        data = load_data()
        if ROUNDS not in data:
            raise LookupError
        if str_round_id not in data[ROUNDS]:
            return None
        json_ref = data[ROUNDS][str_round_id]
        this_round = Round(
            id=round_id,
            name=json_ref["name"],
            matches=[Match.from_id(entry) for entry in json_ref["matches"]],
            # tournament=json_ref["parent_tournament"],
        )
        this_round.start_time = (
            datetime.datetime.fromisoformat(json_ref["start_time"])
            if json_ref["start_time"]
            else None
        )
        this_round.end_time = (
            datetime.datetime.fromisoformat(json_ref["end_time"])
            if json_ref["end_time"]
            else None
        )

        return this_round

    def __str__(self):
        """str method. Returns round's name.

        Returns:
            str: Round name.
        """
        return self.name

    def __repr__(self):
        """repr method. Returns round's ID.

        Returns:
            int: Round ID.
        """
        return self.id


# endregion
