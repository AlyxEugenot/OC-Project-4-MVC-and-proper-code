import datetime
import re
from typing import Self
from chess.model.storage import save_data, load_data, PLAYERS, datetime_to_str


class Player:
    """Player Class."""

    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        birth_date: datetime.date,
        elo: int = 1000,
    ):
        """Player init.

        Args:
            id (str): ID in AB12345 format. (can validate with is_id_valid)
            first_name (str): Player's first name.
            last_name (str): Player's last name.
            birth_date (datetime.date): Player's birth date.
            elo (int, optional): Ranking in official worldwide chess systems.
                Defaults to 1000.
        """
        self.id = id
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.birth_date = birth_date
        self.elo = elo

    def save(self):
        save_data(self.to_json())

    def to_json(self) -> dict:
        """Return json implementation from Player object.

        Args:
            player (Player): Player object to save

        Returns:
            dict: json dict to use for saving
        """
        this_json = {
            PLAYERS: {
                self.id: {
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "birth_date": datetime_to_str(self.birth_date),
                    "elo": self.elo,
                }
            }
        }
        return this_json

    def from_id(player_id: str) -> Self | None:
        """Return Player object from json through id.
        Return None if ID not found.

        Args:
            player_id (str): Player ID (format AB12345)

        Returns:
            Player: Player object
        """
        data = load_data()
        if PLAYERS not in data:
            raise LookupError
        if player_id not in data[PLAYERS]:
            return None
        json_ref = data[PLAYERS][player_id]
        player = Player(
            id=player_id,
            first_name=json_ref["first_name"],
            last_name=json_ref["last_name"],
            birth_date=datetime.date.fromisoformat(json_ref["birth_date"]),
            elo=json_ref["elo"],
        )
        return player

    def is_id_valid(self):
        """Returns True if player ID is in valid format.

        Valid format is 2 letters 5 numbers : AB12345.

        Returns:
            bool: True if the format is correct.
        """
        if re.match("[A-Z]{2}[0-9]{5}$", self.id) is None:
            return False
        else:
            return True

    def __str__(self):
        """str method. Returns first and last name.

        Returns:
            str: "{First name} {Last name}"
        """
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """repr method. Returns player's ID

        Returns:
            str: Player ID.
        """
        return self.id