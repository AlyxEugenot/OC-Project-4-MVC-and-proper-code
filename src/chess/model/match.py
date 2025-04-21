"""Match object."""

import random
from typing import Self
from chess.model import Player
from chess.model.storage import save_data, load_data, MATCHES


class Match:
    """Match class. Used to keep track of match results."""

    def __init__(
        self, _id: int, players: list[Player], white_player: Player = None
    ):
        """Match init.

        Args:
            id (int): Match ID. (len 10)
            players (list[Player, int]): Players and their current match\
                points.
            white_player (Player): Player playing first. Always leave empty.
        """
        self.id = _id
        # self.parent_round = parent_round
        self.players = players
        self.score = {players[0]: 0, players[1]: 0}
        self.white = (
            white_player
            if white_player is not None
            else self.pick_white_player()
        )
        self.save()

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
                self.save()
            return "Tie"

        for p in self.score:
            if p == player:
                self.score[p] += 1
                self.save()
                return f"Player {player} wins."

        raise ValueError

    def save(self):
        """Save match in data.json."""
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
                    "white": self.white.id,
                }
            }
        }
        return this_json

    # pylint: disable=no-self-argument
    def from_id(match_id: int) -> Self | None:
        """Return Match object from json through id.
        Return None if ID not found.

        Args:
            match_id (int): Match ID

        Returns:
            Match | None: Match object or None if not found.
        """
        str_match_id = str(match_id)
        data = load_data()
        if MATCHES not in data:
            raise LookupError
        if str_match_id not in data[MATCHES]:
            return None
        json_ref = data[MATCHES][str_match_id]
        this_match = Match(
            _id=match_id,
            # parent_round=round_from_id(json_ref["parent_round"]),
            players=[
                Player.from_id(player[0]) for player in json_ref["score"]
            ],
            white_player=Player.from_id(json_ref["white"]),
        )
        this_match.score = {
            this_match.players[0]: json_ref["score"][0][1],
            this_match.players[1]: json_ref["score"][1][1],
        }

        this_match.save()
        return this_match

    def is_over(self) -> bool:
        """True if sum of players scores is 1. False if 0."""
        if self.score[self.players[0]] + self.score[self.players[1]] < 1:
            return False
        return True

    def result(self) -> str:
        """Donne le résultat du match.

        Returns:
            str: Résultat du match.
        """
        if self.score[self.players[0]] > 0:
            if self.score[self.players[0]] < 1:
                return "Égalité."
            return f"{str(self.players[0])} a gagné."
        if self.score[self.players[1]] > 0:
            return f"{str(self.players[1])} a gagné."
        else:
            return "Match non joué."

    def __str__(self):
        """str method. Returns match's score.

        Returns:
            str: Match score.
        """
        return (
            f"{str(self.players[0])}"
            f"{"[W]" if self.white == self.players[0] else ""}: "
            f"{self.score[self.players[0]]}, "
            f"{str(self.players[1])}"
            f"{"[W]" if self.white == self.players[1] else ""}: "
            f"{self.score[self.players[1]]}"
        )

    def __repr__(self):
        """repr method. Returns match's ID and score.

        Returns:
            str: Match ID and score.
        """
        return f"{str(self.id)}: {str(self.score)}"
