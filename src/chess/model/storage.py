"""Handles saving of data"""

import json
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SAVED_DATA_PATH = PROJECT_ROOT / "data" / "tournaments" / "data.json"

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


def save_data(data_to_save: dict[str, dict]) -> dict:
    """Update json file with "data_to_save". All values to save must be placed\
        under existing dictionnaries : 'players', 'tournaments', 'rounds',\
            'matches'. KeyError raised otherwise.

    Args:
        data_to_save (dict[str, dict]): data in dict format\
            `players:dict[id:dict]`

    Returns:
        dict: json file saved
    """
    saved_data = load_data()

    for which_dict in data_to_save.keys():
        if which_dict not in saved_data.keys():
            raise KeyError("Wrong input for entry dict")
        for key, value in data_to_save[which_dict].items():
            saved_data[which_dict][str(key)] = value

    with open(SAVED_DATA_PATH, mode="w", encoding="utf-8") as file:
        json.dump(saved_data, file, indent=4)
    return saved_data


def load_data() -> dict[str, dict[str, dict]]:
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


def _setup_json_base() -> dict[str, dict]:
    """Creates necessary json architecture.

    Returns:
        dict: Json file.
    """
    SAVED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    json_file = DICT_STRUCTURE

    with open(SAVED_DATA_PATH, mode="w", encoding="utf-8") as file:
        json.dump(json_file, file, indent=4)
    return json_file


def sort_data() -> dict[str, dict[str, dict]]:
    """Return data sorted in dicts.

    Returns:
        dict: sorted data
    """

    def sort(item, sorting_key):
        return item[1][sorting_key]

    this_json = load_data()
    sorted_json = DICT_STRUCTURE

    for key in this_json:
        match key:
            case "players":
                sorted_json[key] = dict(
                    sorted(
                        this_json[key].items(),
                        key=lambda item: sort(item, "last_name"),
                    )
                )
            case "rounds":
                sorted_json[key] = dict(
                    sorted(
                        this_json[key].items(),
                        key=lambda item: sort(item, "start_time"),
                    )
                )
            case "matches":
                sorted_json[key] = dict(sorted(this_json[key].items()))
                for match in sorted_json[key]:
                    # Sort players by descending score
                    sorted_json[key][match]["score"] = sorted(
                        sorted_json[key][match]["score"],
                        key=lambda item: item[1],
                        reverse=True,
                    )

            case _:
                sorted_json[key] = dict(sorted(this_json[key].items()))

    with open(SAVED_DATA_PATH, mode="w", encoding="utf-8") as file:
        json.dump(sorted_json, file, indent=4)
    return sorted_json


def is_id_valid(_id: str, json_key: str) -> tuple[bool, str]:
    """Verify ID is valid for any data type.

    Args:
        _id (str): ID to verify.
        json_key (str): json_key from data.json.\
            Can be players, rounds, tournaments or matches.

    Raises:
        ValueError: ValueError raised if json_key is wrong.

    Returns:
        tuple[bool, str]: True if id is valid.\
            str references problem to user, is only useful if bool is False.
    """

    if id_already_exists(_id, json_key):
        return (False, "Cet ID existe déjà")

    match json_key:
        case "players":
            return regex_match_id(
                _id,
                regex_expression="[A-Z]{2}[0-9]{5}$",
                error_if_no_match="Le format (AB12345) de l'ID n'est pas bon.",
            )
        case "rounds" | "tournaments":
            return regex_match_id(
                _id,
                regex_expression="[0-9]{6}$",
                error_if_no_match="Le format (123456) de l'ID n'est pas bon.",
            )
        case "matches":
            return regex_match_id(
                _id,
                regex_expression="[0-9]{10}$",
                error_if_no_match=(
                    "Le format (12346578910) de l'ID n'est pas bon."
                ),
            )
        case _:
            raise ValueError(
                "dumbass programmer doesn't know how to put right parameters"
            )


def regex_match_id(
    _id, regex_expression: str, error_if_no_match: str
) -> tuple[bool, str]:
    """For is_id_valid. Verify if _id matches the regex expression.

    Return False and error str if regex doesn't match.

    Args:
        _id (str): ID to verify.
        regex_expression (str): RegEx to match with.
        error_if_no_match (str): Error returned if no match.

    Returns:
        tuple[bool, str]: True if id matches regex expression.\
            str returned if bool is False.
    """
    if re.match(regex_expression, _id) is None:
        return (False, error_if_no_match)
    return (True, "")


def id_already_exists(_id, dict_key: str) -> bool:
    """Check if id exists in data.json.

    Args:
        _id (str): ID to check.
        dict_key (str): json_key from data.json.\
            Can be players, rounds, tournaments or matches.

    Raises:
        ValueError: ValueError raised if json_key is wrong.

    Returns:
        bool: True if id is already present in saved data.
    """
    this_json = load_data()
    if dict_key not in this_json.keys():
        raise ValueError
    return _id in this_json[dict_key].keys()
