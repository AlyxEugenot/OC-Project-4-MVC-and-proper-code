"""All callbacks to do with model."""

import sys
import typing
import chess.model
import chess.model.generate
import chess.model.storage
from chess import utils

if typing.TYPE_CHECKING:
    from chess.controller.menus._abstract import Menu


def add_player_to_tournament(
    player_id: str, tournament: chess.model.Tournament
) -> chess.model.Player | None:
    """Add player to tournament if exist in data.json.

    Args:
        player_id (str): Player ID to add. (format AB12345)
        tournament (chess.model.Tournament): Tournament to add players to.

    Returns:
        chess.model.Player | None: Return Player if added to tournament.\
            Else return None.
    """
    player = chess.model.Player.from_id(player_id)
    if player is not None:
        tournament.add_player(player)
        tournament.save()
        return player
    return None


def update_tournament_scores(
    tournament: chess.model.Tournament,
    finished_matches: list[chess.model.Match],
):
    """Update tournament scores from matches results on round end.

    Args:
        tournament (chess.model.Tournament): Tournament to update.
        finished_matches (list[chess.model.Match]): All finished matches.
    """
    for match in finished_matches:
        for player in match.players:
            for t_player in tournament.players:
                if t_player[0].id == player.id:
                    t_player[1] += match.score[player]
                    break
    tournament.save()


def start_new_round(tournament: chess.model.Tournament) -> chess.model.Round:
    """Set the round when beginning it by generating match pairs and round ID.

    Args:
        tournament (chess.model.Tournament): Tournament to set new round in.

    Returns:
        chess.model.Round: Round set up.
    """
    generated_pairs = utils.generate_pairs_for_new_round(tournament)
    matches = []
    for opponents in generated_pairs:
        match_id = chess.model.generate.generate_available_id(
            chess.model.storage.MATCHES
        )
        matches.append(chess.model.Match(_id=match_id, players=opponents))

    round_id = chess.model.generate.generate_available_id(
        chess.model.storage.ROUNDS
    )
    new_round = chess.model.Round(
        _id=round_id,
        name=f"Round {len(tournament.rounds)+1}",
        matches=matches,
    )
    tournament.rounds.append(new_round)
    return new_round


# region Reports callbacks
def report_players(
    player_ids: list[str] = None,
) -> list[tuple[str, str, str, str, int]]:  # all players if None
    """Get list of player info from data.json.
    All players if player_ids is None.

    First tuple element is info type (headers).

    Returned tuples are:
        ID
        Last name
        First name
        Birth date
        Elo

    Args:
        player_ids (list[str], optional): IDs to get player info from.
            Get all players if None. Defaults to None.

    Returns:
        list[tuple[str, str, str, str, int]]: Player info. First list element
            is info type (headers). Returned tuples are
            (ID, Last name, First name, Birth date, Elo)
    """
    players_json = chess.model.storage.sort_data()[chess.model.storage.PLAYERS]

    returned_list = [["ID", "Nom", "Prénom", "Date de naissance", "Elo"]]
    if player_ids is not None:
        players_json = utils.slim_json_dict_by_ids(players_json, player_ids)

    for key, value in players_json.items():
        returned_list.append(
            [
                key,
                value["last_name"],
                value["first_name"],
                f"{utils.json_date_to_str(value["birth_date"])}",
                value["elo"],
            ]
        )

    return returned_list


def report_players_from_tournament(
    tournament_id: str,
) -> list[tuple[str, str, str, str, int]]:
    """Get list of player info of tournament from data.json.

    First tuple element is info type (headers).

    Returned tuples are:
        ID
        Last name
        First name
        Birth date
        Elo


    Args:
        tournament_id (str): Tournament ID as str to get info from.

    Returns:
        list[tuple[str, str, str, str, int]]: Player info of tournament.
            First list element is info type (headers). Returned tuples are
            (ID, Last name, First name, Birth date, Elo)
    """
    tournaments_json = chess.model.storage.load_data()[
        chess.model.storage.TOURNAMENTS
    ]

    try:
        player_score = tournaments_json[tournament_id]["players"]
    except KeyError:
        print(
            "L'ID de tournoi n'existe pas. Les IDs qui fonctionnent sont "
            f"{", ".join(tournaments_json.keys())}."
        )
        return [["Tournoi"], ["non trouvé."]]

    player_ids = [x[0] for x in player_score]

    return report_players(player_ids)


def report_rounds_from_tournament(
    tournament_id: str, match_is_int: bool = True
) -> list[tuple[int, str, str, str, str]]:  # multiline if match_is_int False
    """Get list of round info of tournament from data.json.

    If match_is_int is False, return all match info as well. Return match IDs
    instead if True.

    First tuple element is info type (headers).

    Returned tuple is:
        ID
        Round name
        Matches (format "player1[W]: 1, player2: 0" if match_is_int is False)
        Round beginning datetime
        Round ending datetime

    Args:
        tournament_id (str): Tournament ID as str to get info from.
        match_is_int (bool, optional):  If False, return all match info.
            If True, return match IDs instead. Defaults to True.

    Returns:
        list[tuple[int, str, str, str, str]]: Round info. First tuple element
            is info type (headers). Returned tuples are
            (ID, Round name, Matches, Round beginning datetime,
            Round ending datetime)
    """

    json = chess.model.storage.sort_data()
    tournaments_json = json[chess.model.storage.TOURNAMENTS]
    rounds_json = json[chess.model.storage.ROUNDS]

    try:
        rounds = tournaments_json[tournament_id]["rounds"]
    except KeyError:
        print(
            "L'ID de tournoi n'existe pas. Les IDs qui fonctionnent sont "
            f"{", ".join(tournaments_json.keys())}."
        )
        return [["Tournoi"], ["non trouvé."]]

    returned_list = [["ID", "Nom", "Matchs", "Début du round", "Fin du round"]]
    rounds_json = utils.slim_json_dict_by_ids(
        rounds_json, [str(r) for r in rounds]
    )

    for key, value in rounds_json.items():
        if match_is_int:
            matches_str = ", ".join([str(m) for m in value["matches"]])
        else:
            matches_str = []
            for match_id in value["matches"]:
                match_json = json[chess.model.storage.MATCHES][str(match_id)]
                # ex: player1[W]: 1, player2: 0
                match_result = (
                    f"{str(match_json["score"][0][0])}"
                    f"{"[W]" if match_json["white"] == match_json["score"][0][0] else ""}: "  # noqa
                    f"{match_json["score"][0][1]}, "
                    f"{str(match_json["score"][1][0])}"
                    f"{"[W]" if match_json["white"] == match_json["score"][1][0] else ""}: "  # noqa
                    f"{match_json["score"][1][1]}"
                )
                matches_str.append(
                    f"------ {str(match_id)} ------\n{match_result}"
                )

            matches_str = "\n".join(matches_str)

        returned_list.append(
            [
                key,
                value["name"],
                matches_str,
                f"{utils.json_datetime_to_str(value["start_time"])}",
                f"{utils.json_datetime_to_str(value["end_time"])}",
            ]
        )
    return returned_list


def report_matches_from_round(round_id: str) -> list[tuple[int, str, str]]:
    """Get list of match info of round from data.json.

    First tuple element is info type (headers).

    Returned tuple is:
        ID
        Players and scores
        White player

    Args:
        round_id (str): Round ID as str to get info from.

    Returns:
        list[tuple[int, str, str]]: Match info. First tuple element is info
            type (headers). Returned tuples are
            (ID, Players and scores, White player)
    """
    json = chess.model.storage.sort_data()
    rounds_json = json[chess.model.storage.ROUNDS]
    matches_json = json[chess.model.storage.MATCHES]

    try:
        match_ids = rounds_json[round_id]["matches"]
    except KeyError:
        print(
            "L'ID de round n'existe pas. Les IDs qui fonctionnent sont "
            f"{", ".join(rounds_json.keys())}."
        )
        return [["Round"], ["non trouvé."]]

    returned_list = [["ID", "Joueurs: Score", "Joueur blanc"]]
    matches_json = utils.slim_json_dict_by_ids(
        matches_json, [str(m) for m in match_ids]
    )

    for key, value in matches_json.items():
        returned_list.append(
            [
                key,
                f"{utils.nested_list_to_str(value["score"], ": ", " vs ")}",
                value["white"],
            ]
        )

    return returned_list


def report_tournaments(
    tournament_id: str = None,
) -> list[tuple[str, str, str, str, str, str, str, str, str]]:
    """Get list of tournament info from data.json.
    All tournaments if tournament_id is None.

    First tuple element is info type (headers).

    Returned tuple is:
        ID
        Tournament name
        Players and scores
        Rounds
        Address
        Round amount
        Description
        Tournament beginning datetime
        Tournament ending datetime

    Args:
        tournament_id (str, optional): ID to get tournament info from.
            Get all tournaments if None. Defaults to None.

    Returns:
        list[ tuple[str, str, str, str, str, str, str, str, str] ]: Tournament
            info. First tuple element is info type (headers). Returned tuples
            are (ID, Tournament name, Players and scores, Rounds, Address,
            Round amount, Description, Tournament beginning datetime,
            Tournament ending datetime)
    """
    tournaments_json = chess.model.storage.sort_data()[
        chess.model.storage.TOURNAMENTS
    ]

    returned_list = [
        [
            "ID",
            "Nom",
            "Joueurs + Scores",
            "Rounds",
            "Adresse",
            "Nombre de rounds",
            "Description",
            "Début du tournoi",
            "Fin du tournoi",
        ]
    ]
    if tournament_id is not None:
        try:
            tournaments_json = {tournament_id: tournaments_json[tournament_id]}
        except KeyError:
            print(
                "L'ID de tournoi n'existe pas. Les IDs qui fonctionnent sont "
                f"{", ".join(tournaments_json.keys())}."
            )
            returned_list.append(
                [
                    f"{tournament_id} n'existe pas.",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                    "NA",
                ]
            )
            return returned_list

    for key, value in tournaments_json.items():
        returned_list.append(
            [
                key,
                value["name"],
                f"{utils.nested_list_to_str(value["players"])}",
                f"{"\n".join([str(x) for x in value["rounds"]])}",
                f"{str(chess.model.Address.from_json(value["localization"]))}",
                value["rounds_amount"],
                value["description"],
                f"{utils.json_datetime_to_str(value["start_time"])}",
                f"{utils.json_datetime_to_str(value["end_time"])}",
            ]
        )

    return returned_list


# endregion


# region View callbacks
def quit_program(my_print: typing.Callable):
    """view.inputs.regular_inputs method.

    Quit program.

    Args:
        my_print (typing.Callable): view.my_print as in view to print
            as expected.
    """
    my_print("\nArrêt du programme...")
    sys.exit(0)


def execute_main_menu(
    main_menu: "Menu",
    current_menu_arborescence: list[str],
    menu_header: typing.Callable,
):
    """view.inputs.regular_inputs method.

    Execute main menu.

    Args:
        main_menu (Menu): Menu to execute.
        current_menu_arborescence (list[str]): view.current_menu_arborescence
            object.
        my_print (typing.Callable): view.my_print as in view to print
            as expected.
        menu_header (typing.Callable): view.my_print_header as in view to
            print headers as expected.
    """
    current_menu_arborescence.clear()
    current_menu_arborescence.append("Menu principal")
    menu_header()
    main_menu.execute()


def cancel(
    current_menu: "Menu",
    current_menu_arborescence: list[str],
    my_print: typing.Callable,
    menu_header: typing.Callable,
):
    """view.inputs.regular_inputs method.

    Execute last menu. (Execute this menu if current menu item is action.
    Else, execute parent)

    Update header and view.current_menu_arborescence on the way.

    Args:
        current_menu (Menu): Current menu. (execute this or parents' execute)
        current_menu_arborescence (list[str]): view.current_menu_arborescence
            object.
        my_print (typing.Callable): view.my_print as in view to print
            as expected.
        menu_header (typing.Callable): view.my_print_header as in view to
            print headers as expected.
    """
    my_print("retour...")
    if current_menu_arborescence[-1].startswith("action"):
        menu = current_menu
    else:
        if current_menu.parent is not None:
            menu = current_menu.parent
        else:
            # if we were already in main_menu
            current_menu_arborescence.append("")
            menu = current_menu

    current_menu_arborescence.pop()
    menu_header()
    menu.execute()


# endregion
