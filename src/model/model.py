# TODO insert docstring when classes are more fleshed out.
import datetime
import re
import random

# import generate


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


class Address:
    """Address class to French address standard: AFNOR NF 10-011.

    All fields should be 38 characters max str.
    """

    def __init__(
        self,
        addressee_id: str,
        delivery_point: str,
        house_nb_street_name: str,
        postcode: str,
        additional_geo_info: str = "",
        additional_delivery_info: str = "",
        country_name: str = "France",
    ):
        """French address standard. All fields should be 38 characters max.

        Args:
            addressee_id (str): 1. Addressee ID: civility, title or quality +\
                firstname+ surname. ex: M. Valéry DUPONT
            delivery_point (str): 2. Identification complement: appt nb,\
                letter box, stair, corridor. ex: Appartment 12 Stairs C
            house_nb_street_name (str): 4. Number and street name.\
                ex: 1 avenue des champs élysées
            postcode (str): 6. Postal code and destination locality.\
                ex: 75001 PARIS
            additional_geo_info (str, optional): 3. outside ID complement:\
                entry, tower, building, residence. ex: Résidence Les Tilleuls.\
                    Defaults to "".
            additional_delivery_info (str, optional):
                5. Hamlet (lieu-dit) or particular distribution service:\
                post box, poste restante. ex: La Chaise Dieu. Defaults to "".
            country_name (str, optional): 7. Country name. Defaults to "France".
        """
        self.addressee_id = addressee_id
        self.delivery_point = delivery_point
        self.additional_geo_info = additional_geo_info
        self.house_nb_street_name = house_nb_street_name
        self.additional_delivery_info = additional_delivery_info
        self.postcode = postcode
        self.country_name = country_name

    def __str__(self):
        """str method. Address formatted.

        Returns:
            str: Address formatted.
        """
        complete_address = [
            self.addressee_id,
            self.delivery_point,
            self.additional_geo_info,
            self.house_nb_street_name,
            self.additional_delivery_info,
            self.postcode,
            self.country_name,
        ]
        filled_address = []
        for element in complete_address:
            if element != "" or element is None:
                filled_address.append(element)
        return "\n".join(filled_address)


class Tournament:
    """Tournament class. Tournaments are split in multiple rounds."""

    def __init__(
        self,
        id: int,
        name: str,
        players: list[Player],
        localization: Address,
        rounds_amount: int = 4,
        description: str = "",
    ):
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
        self.players = [[player,0] for player in players]
        self.rounds = []
        self.localization = localization
        self.rounds_amount = rounds_amount

        self.start_time = None
        self.end_time = None

        if description == "":
            self.description = (
                f"Tournament {name} at {localization.postcode}"
                f"the {self.start_time}."
            )
        else:
            self.description = description

    def add_player(self, player:Player):
        self.players.append([player,0])

    def start_tournament(self):
        self.start_time = datetime.datetime.now()

    def end_tournament(self):
        self.end_time = datetime.datetime.now()

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


class Round:
    """Round class. Rounds are composed of multiple matches."""

    def __init__(self, id: int, name: str, tournament: Tournament):
        """Round init.

        Args:
            id (int): Round ID.
            name (str): Round Name. ex: "Round 1"
            tournament (Tournament): Tournament the round is a part of.
        """
        self.id = id
        self.name = name
        self.parent_tournament = tournament

        self.start_time = None
        self.end_time = None
        self.matches = []

        self.start_round()

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


class Match:
    """Match class. Used to keep track of match results."""

    def __init__(self, id: int, parent_round: Round, players: list[Player]):
        """Match init.

        Args:
            id (int): Match ID.
            parent_round (Round): Round the match is a part of.
            players (list[Player, int]): Players and their current match points.
        """
        self.id = id
        self.parent_round = parent_round
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
