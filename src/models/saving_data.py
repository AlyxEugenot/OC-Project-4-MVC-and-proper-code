"""Handles saving of data"""

import json
from pathlib import Path
import datetime
from models.model import Player, Tournament, Round, Match, Address

PROJECT_ROOT = Path(__file__).parent.parent.parent
SAVED_DATA_PATH = PROJECT_ROOT / "data" / "data.json"

PLAYERS = "players"
TOURNAMENTS = "tournaments"
ROUNDS = "rounds"
MATCHES = "matches"
ADDRESS = "address"

DICT_STRUCTURE = {
    PLAYERS: {},
    TOURNAMENTS: {},
    ROUNDS: {},
    MATCHES: {},
}


def save_data(data_to_save: dict) -> dict:
    """Update json file with "data_to_save". All values to save must be placed under existing dictionnaries : 'players', 'tournaments', 'rounds', 'matches'. KeyError raised otherwise.

    Args:
        data_to_save (dict): data in dict format `key:value,...`

    Returns:
        dict: json file saved
    """
    saved_data = load_data()

    for which_dict in data_to_save.keys():
        if which_dict not in saved_data.keys():
            raise KeyError("Wrong input for entry dict")
        for key, value in data_to_save[which_dict].items():
            saved_data[which_dict][key] = value

    with open(SAVED_DATA_PATH, mode="w", encoding="utf-8") as file:
        new_file = json.dump(saved_data, file, indent=4)
    return saved_data


def load_data() -> dict:
    """Load and return json file. Create base if nonexistent.

    Returns:
        dict: json save file
    """
    if SAVED_DATA_PATH.exists():
        with open(SAVED_DATA_PATH, mode="r", encoding="utf-8") as file:
            result = json.load(file)
        return result
    else:
        return _setup_json_base()


def _setup_json_base() -> dict:
    """Creates necessary json architecture.

    Returns:
        dict: Json file.
    """
    SAVED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    json_file = DICT_STRUCTURE

    with open(SAVED_DATA_PATH, mode="w", encoding="utf-8") as file:
        json.dump(json_file, file, indent=4)
    return json_file


def sort_data() -> dict:
    """Return data sorted in dicts.

    Returns:
        dict: sorted data
    """
    this_json = load_data()
    sorted_json = DICT_STRUCTURE

    for key in this_json:
        sorted_json[key] = dict(sorted(this_json[key].items()))

    with open(SAVED_DATA_PATH, mode="w", encoding="utf-8") as file:
        json.dump(sorted_json, file, indent=4)
    return sorted_json


# region player
def player_to_json(player: Player) -> dict:
    """Return json implementation from Player object.

    Args:
        player (Player): Player object to save

    Returns:
        dict: json dict to use for saving
    """
    this_json = {
        PLAYERS: {
            player.id: {
                "first_name": player.first_name,
                "last_name": player.last_name,
                "birth_date": datetime_to_str(player.birth_date, timespec="auto"),
                "elo": player.elo,
            }
        }
    }
    return this_json


def player_from_id(player_id: str) -> Player:
    """Return Player object from json through id.

    Args:
        player_id (str): Player ID (format AB12345)

    Returns:
        Player: Player object
    """
    json_ref = load_data()[PLAYERS][player_id]
    player = Player(
        id=player_id,
        first_name=json_ref["first_name"],
        last_name=json_ref["last_name"],
        birth_date=datetime.date.fromisoformat(json_ref["birth_date"]),
        elo=json_ref["elo"],
    )
    return player


# endregion


# region address
def address_to_json(address: Address) -> dict:
    """Return json implementation from Address object.

    Args:
        address (Address): Adress object to save

    Returns:
        dict: json dict to use for saving
    """
    this_json = {
        "addressee_id": address.addressee_id,
        "delivery_point": address.delivery_point,
        "additional_geo_info": address.additional_geo_info,
        "house_nb_street_name": address.house_nb_street_name,
        "additional_delivery_info": address.additional_delivery_info,
        "postcode": address.postcode,
        "country_name": address.country_name,
    }
    return this_json


def address_from_json(address: dict) -> Address:
    """Return Address object from json.

    Args:
        address (dict): Address dict

    Returns:
        Address: Address object
    """
    returned_address = Address(
        addressee_id=address["addressee_id"],
        delivery_point=address["delivery_point"],
        additional_geo_info=address["additional_geo_info"],
        house_nb_street_name=address["house_nb_street_name"],
        additional_delivery_info=address["additional_delivery_info"],
        postcode=address["postcode"],
        country_name=address["country_name"],
    )
    return returned_address


# endregion


# region tournament
def tournament_to_json(tournament: Tournament) -> dict:
    """Return json implementation from Tournament object.

    Args:
        tournament (Tournament): Tournament object to save

    Returns:
        dict: json dict to use for saving
    """
    this_json = {
        TOURNAMENTS: {
            tournament.id: {
                "name": tournament.name,
                "players": [[player[0].id, player[1]] for player in tournament.players],
                "rounds": [round.id for round in tournament.rounds],
                "localization": address_to_json(tournament.localization),
                "rounds_amount": tournament.rounds_amount,
                "description": tournament.description,
                "start_time": datetime_to_str(tournament.start_time),
                "end_time": datetime_to_str(tournament.end_time),
            }
        }
    }
    return this_json


def tournament_from_id(tournament_id: str) -> Tournament:
    """Return Tournament object from json through id.

    Args:
        tournament_id (str): Tournament ID

    Returns:
        Tournament: Tournament object
    """
    json_ref = load_data()[TOURNAMENTS][tournament_id]
    tournament = Tournament(
        id=tournament_id,
        name=json_ref["name"],
        players=[
            [player_from_id(player[0]), player[1]] for player in json_ref["players"]
        ],
        localization=address_from_json(json_ref["localization"]),
        rounds_amount=json_ref["rounds_amount"],
        description=json_ref["description"],
    )
    tournament.start_time = (datetime.datetime.fromisoformat(json_ref["start_date"]),)
    tournament.end_time = datetime.datetime.fromisoformat(json_ref["end_date"])

    return tournament


# endregion


# region round
def round_to_json(round: Round) -> dict:
    """Return json implementation from Round object.

    Args:
        round (Round): Round object to save

    Returns:
        dict: json dict to use for saving
    """
    this_json = {
        ROUNDS: {
            round.id: {
                "name": round.name,
                "matches": [_match.id for _match in round.matches],
                "parent_tournament": round.parent_tournament,
                "start_time": datetime_to_str(round.start_time),
                "end_time": datetime_to_str(round.end_time),
            }
        }
    }
    return this_json


def round_from_id(round_id: str) -> Round:
    """Return Round object from json through id.

    Args:
        round_id (str): Round ID

    Returns:
        Round: Round object
    """
    json_ref = load_data()[ROUNDS][round_id]
    this_round = Round(
        id=round_id,
        name=json_ref["name"],
        tournament=json_ref["parent_tournament"],
    )
    this_round.matches = [match_from_id(entry) for entry in json_ref["matches"]]
    this_round.start_time = datetime.datetime.fromisoformat(json_ref["start_time"])
    this_round.end_time = datetime.datetime.fromisoformat(json_ref["end_time"])

    return this_round


# endregion


# region match
def match_to_json(match: Match) -> dict:
    """Return json implementation from Match object.

    Args:
        match (Match): Match object to save

    Returns:
        dict: json dict to use for saving
    """
    this_json = {
        MATCHES: {
            match.id: {
                "parent_round": match.parent_round.id,
                "score": [
                    [match.players[0].id, match.score[match.players[0]]],
                    [match.players[1].id, match.score[match.players[1]]],
                ],
            }
        }
    }
    return this_json


def match_from_id(match_id: str) -> Match:
    """Return Match object from json through id.

    Args:
        match_id (str): Match ID

    Returns:
        Match: Match object
    """
    json_ref = load_data()[MATCHES][match_id]
    this_match = Match(
        id=match_id,
        parent_round=round_from_id(json_ref["parent_round"]),
        players=[player_from_id(player[0]) for player in json_ref["score"]],
    )
    this_match.score = {
        this_match.players[0]: json_ref["score"][0][1],
        this_match.players[1]: json_ref["score"][1][1],
    }
    return this_match


# endregion


def datetime_to_str(date: datetime.datetime, timespec: str = "seconds") -> str:
    """Return datetime or date to isoformat. 
    
    Return None if date is None, to let empty data stay empty.

    Args:
        date (datetime.datetime): datetime or date to stringify
        timespec (str, optional): "seconds" if type(date) is datetime. "auto" if type(date) is date. Defaults to "seconds".

    Returns:
        str: date to isoformat. None if None
    """
    if date is not None:
        return date.isoformat(timespec=timespec)
    else:
        return None


if __name__ == "__main__":
    temp = {
        PLAYERS: {"ID12345": {"a": 1, "b": 2}},
        TOURNAMENTS: {"pwet": 1},
        ROUNDS: {},
        MATCHES: {},
    }
    save_data(temp)
    pass
