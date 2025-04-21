"""Utils."""

from datetime import datetime
import typing

if typing.TYPE_CHECKING:
    import chess.model


def generate_pairs_for_new_round(
    tournament: "chess.model.Tournament",
) -> list[tuple["chess.model.Player", "chess.model.Player"]]:
    """Generate pairs for new round from players in tournament.

    Verify players have not matched before.

    Args:
        tournament (Tournament): Tournament to generate new player pairs in.

    Returns:
        list[tuple[Player, Player]]: List of Player pairs
    """
    # sort by player score
    sorted_players: list = sorted(
        tournament.players, key=lambda i: i[1], reverse=True
    )
    duos = []
    # assign players by duo
    for i in range(0, len(sorted_players), 2):
        player1_idx, player2_idx = 0, 1
        # if enough players to assign other players
        if len(sorted_players) // 2 > 1:
            # while player 1 already met his opponent:
            while tournament.players_already_met(
                sorted_players[player1_idx][0], sorted_players[player2_idx][0]
            ):
                # get next possible player
                player2_idx += 1

                # if no more players available,
                # get 1st one given (closest score)
                try:
                    sorted_players[player2_idx]
                except IndexError:
                    player2_idx = 1
                    break

        duos.append(
            [sorted_players[player1_idx][0], sorted_players[player2_idx][0]]
        )
        sorted_players.pop(player2_idx)
        sorted_players.pop(player1_idx)

    return duos


def nested_list_to_str(
    nested_list: list[list[str]],
    inner_join_str: str = " ",
    outer_join_str: str = "\n",
) -> str:
    """Decompose a nested list to a single str joined with inner_join_str and
    outer_join_str.

    Args:
        nested_list (list[list[str]]): Nested list to decompose.
        inner_join_str (str, optional): inner join char. Defaults to " ".
        outer_join_str (str, optional): outer join char. Defaults to "\\n".

    Returns:
        str: Decomposed nested list joined with inner_join_str and
        outer_join_str.
    """
    inner_strs = []
    for outer in nested_list:
        inner_strs.append(inner_join_str.join([str(x) for x in outer]))
    final_str = outer_join_str.join(inner_strs)
    return final_str


def json_date_to_str(json_date: str) -> str:
    """Adapt date in json to str in "day-month-year" format.

    Args:
        json_date (str): json date to adapt as str.

    Returns:
        str: Date in "day-month-year" format.
    """
    if json_date is None:
        return "None"
    return datetime.fromisoformat(json_date).strftime("%d-%m-%Y")


def json_datetime_to_str(json_datetime: str) -> str:
    """Adapt json datetime to str in "day-month-year hour:minute" format.

    Args:
        json_datetime (str): json datetime to adapt as str.

    Returns:
        str: Date in "day-month-year hour:minute" format.
    """
    if json_datetime is None:
        return "None"
    return datetime.fromisoformat(json_datetime).strftime("%d-%m-%Y %H:%M")


def slim_json_dict_by_ids(
    dict_to_slim: dict[str, dict], ids: list
) -> dict[str, dict]:
    """Cut down dict to only retain list of IDs.

    Args:
        dict_to_slim (dict[str, dict]): Dict to cut down.
        ids (list): List of IDs to keep from dict.

    Raises:
        ValueError: ValueError raised if any ID not found.

    Returns:
        dict[str, dict]: Reduced dict.
    """
    reduced_dict = {}
    for _id in ids:
        try:
            reduced_dict[_id] = dict_to_slim[_id]
        except ValueError:
            print(f"{_id} non trouvé.")
    return reduced_dict


def is_empty_string(string_to_test: str) -> bool:
    """True if str is equals to "" or is None.

    Args:
        string_to_test (str): str to test if is empty or None.

    Returns:
        bool: True if str is equals to "" or is None.
    """
    if string_to_test == "" or string_to_test is None:
        return True
    return False


def datetime_to_isoformat(
    _datetime: datetime,
) -> str:
    """Return datetime or date to isoformat.

    Return None if date is None, to let empty data stay empty.

    Args:
        _datetime (datetime.datetime): datetime to stringify

    Returns:
        str: date to isoformat. None if None
    """
    if _datetime is not None:
        return _datetime.isoformat()
    return None
