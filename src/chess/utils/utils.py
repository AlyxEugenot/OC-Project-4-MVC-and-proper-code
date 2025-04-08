from datetime import datetime
import typing

if typing.TYPE_CHECKING:
    import chess.model


def generate_pairs_for_new_round(
    tournament: "chess.model.Tournament",
) -> list[list["chess.model.Player"]]:
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
    inner_strs = []
    for outer in nested_list:
        inner_strs.append(inner_join_str.join([str(x) for x in outer]))
    final_str = outer_join_str.join(inner_strs)
    return final_str


def json_date_to_str(json_date: str) -> str:
    if json_date == "null":
        return "null"
    else:
        return datetime.fromisoformat(json_date).strftime("%d-%m-%Y")


def slim_json_dict_by_ids(
    dict_to_slim: dict[str, dict], ids: list
) -> dict[str, dict]:
    reduced_dict = {}
    for id in ids:
        try:
            reduced_dict[id] = dict_to_slim[id]
        except KeyError:
            print(f"{id} non trouvé.")
    return reduced_dict


def is_empty_string(string_to_test: str) -> bool:
    if string_to_test == "" or string_to_test is None:
        return True
    else:
        return False


def json_datetime_to_str(json_datetime: str) -> str:
    if json_datetime is None:
        return "None"
    else:
        return datetime.fromisoformat(json_datetime).strftime("%d-%m-%Y %H:%M")


def datetime_to_isoformat(
    datetime: datetime,
) -> str:
    """Return datetime or date to isoformat.

    Return None if date is None, to let empty data stay empty.

    Args:
        date (datetime.datetime): datetime or date to stringify

    Returns:
        str: date to isoformat. None if None
    """
    if datetime is not None:
        return datetime.isoformat()
    else:
        return None
