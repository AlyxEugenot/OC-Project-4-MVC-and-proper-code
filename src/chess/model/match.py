import typing
import random
from typing import Self
from chess.model import Player
from chess.model.storage import save_data, load_data, MATCHES


class Match:
    """Match class. Used to keep track of match results."""

    def __init__(
        self, id: int, players: list[Player]
    ):  # parent_round: Round, players: list[Player]):
        """Match init.

        Args:
            id (int): Match ID.
            parent_round (Round): Round the match is a part of.
            players (list[Player, int]): Players and their current match points.
        """
        self.id = id
        # self.parent_round = parent_round
        self.players = players
        self.score = [{players[0]: 0, players[1]: 0}]

    def pick_white_player(self) -> Player:
        """Pick white player at random.

        Returns:
            Player: White Player.
        """
        return random.choice(self.players)

    def declare_winner(self, player: Player) -> str:
        """Declare winner. Tie if player is None.

        Args:
            player (Player): Winning player. Tie if None.

        Raises:
            ValueError: Error if no winning player and tie does not trigger.

        Returns:
            str: Match result.
        """
        if player is None:
            for p in self.score:
                self.score[p] += 0.5
            return "Tie"

        for p in self.score:
            if p == player:
                self.score[p] += 1
            return f"Player {player} wins."

        raise ValueError

    def save(self):
        save_data(self.to_json())

    def to_json(self) -> dict:
        """Return json implementation from Match object.

        Args:
            match (Match): Match object to save

        Returns:
            dict: json dict to use for saving
        """
        this_json = {
            MATCHES: {
                self.id: {
                    # "parent_round": self.parent_round.id,
                    "score": [
                        [self.players[0].id, self.score[self.players[0]]],
                        [self.players[1].id, self.score[self.players[1]]],
                    ],
                }
            }
        }
        return this_json

    def from_id(match_id: int) -> Self:
        """Return Match object from json through id.
        Return None if ID not found.

        Args:
            match_id (int): Match ID

        Returns:
            Match: Match object
        """
        str_match_id = str(match_id)
        data = load_data()
        if MATCHES not in data:
            raise LookupError
        if str_match_id not in data[MATCHES]:
            return None
        json_ref = data[MATCHES][str_match_id]
        this_match = Match(
            id=match_id,
            # parent_round=round_from_id(json_ref["parent_round"]),
            players=[Player.from_id(player[0]) for player in json_ref["score"]],
        )
        this_match.score = {
            this_match.players[0]: json_ref["score"][0][1],
            this_match.players[1]: json_ref["score"][1][1],
        }
        return this_match

    def __str__(self):
        """str method. Returns match's score.

        Returns:
            str: Match score.
        """
        return str(self.score)

    def __repr__(self):
        """repr method. Returns match's ID.

        Returns:
            int: Match ID.
        """
        return self.id
