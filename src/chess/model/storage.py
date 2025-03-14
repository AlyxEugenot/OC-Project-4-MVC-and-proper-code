"""Handles saving of data"""

import json
from pathlib import Path
import datetime

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
    """Update json file with "data_to_save". All values to save must be placed \
        under existing dictionnaries : 'players', 'tournaments', 'rounds',\
            'matches'. KeyError raised otherwise.

    Args:
        data_to_save (dict[str, dict]): data in dict format `players:dict[id:dict]`

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
        new_file = json.dump(saved_data, file, indent=4)
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
        if key == PLAYERS:
            sorted_json[key] = dict(
                sorted(this_json[key].items(), key=lambda item: sort(item, "last_name"))
            )
        else:
            sorted_json[key] = dict(sorted(this_json[key].items()))

    with open(SAVED_DATA_PATH, mode="w", encoding="utf-8") as file:
        json.dump(sorted_json, file, indent=4)
    return sorted_json


def id_already_exists(id, dict_key: str):
    this_json = load_data()
    if dict_key not in this_json.keys():
        raise LookupError
    if id in this_json[dict_key].keys():
        return True
    else:
        return False


def datetime_to_str(
    date: datetime.datetime,
) -> str:  # FIXME effacer dans la docstring aussi, timespec: str = "seconds") -> str:
    """Return datetime or date to isoformat.

    Return None if date is None, to let empty data stay empty.

    Args:
        date (datetime.datetime): datetime or date to stringify
        timespec (str, optional): "seconds" if type(date) is datetime. "auto" if type(date) is date. Defaults to "seconds".

    Returns:
        str: date to isoformat. None if None
    """
    if date is not None:
        return date.isoformat()
    else:
        return None
