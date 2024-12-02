import datetime
import re
import random


class Player:
    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        birth_date: datetime.date,
        elo: int = 1000,
    ):
        self.id = id
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.birth_date = birth_date
        self.elo = elo

    def is_id_valid(self):
        if re.match("[A-Z]{2}[0-9]{5}$", self.id) is None:
            return False
        else:
            return True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return self.id


class Address:
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
        self.addressee_id = addressee_id
        self.delivery_point = delivery_point
        self.additional_geo_info = additional_geo_info
        self.house_nb_street_name = house_nb_street_name
        self.additional_delivery_info = additional_delivery_info
        self.postcode = postcode
        self.country_name = country_name


class Tournament:
    def __init__(
        self,
        id: int,
        name: str,
        players: list[Player],
        localization: Address,
        rounds_amount: int = 4,
        *,
        description: str,
    ):
        self.id = id
        self.name = name
        self.players = players
        self.localization = localization
        self.rounds_amount = rounds_amount
        self.description = description

        self.start_date = datetime.date.today()
        self.end_date = None
        self.round_list = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.id


class Round:
    def __init__(self, id: int, name: str, tournament: Tournament):
        self.id = id
        self.name = name
        self.parent_tournament = tournament

        self.start_time = None
        self.end_time = None
        self.matches = []

        self.start_round()

    def start_round(self):
        self.start_time = datetime.datetime.now()
        return self.start_time

    def end_round(self):
        self.end_time = datetime.datetime.now()
        return self.end_time

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.id


class Match:
    def __init__(self, id: int, parent_round: Round, players: list[Player]):
        self.id = id
        self.parent_round = parent_round
        self.players = players
        self.score = [{players[0]: 0, players[1]: 0}]

    def pick_white_player(self) -> Player:
        return random.choice(self.players)

    def declare_winner(self, player: Player) -> str:
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
        return str(self.score)

    def __repr__(self):
        return self.id
