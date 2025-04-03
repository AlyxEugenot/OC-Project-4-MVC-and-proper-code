import chess.model
import chess.model.storage
import chess.model.generate
from datetime import date, datetime


def add_player_to_tournament(
    player_id: str, tournament: chess.model.Tournament
) -> chess.model.Player | None:
    player = chess.model.Player.from_id(player_id)
    if player is not None:
        tournament.add_player(player)
        tournament.save()
        return player
    else:
        return None


def list_players(
    player_ids: list[str] = None,
) -> tuple[str, str, str, str, int]:  # all players if None
    players_json = chess.model.storage.sort_data()[chess.model.storage.PLAYERS]

    returned_list = [["ID", "Nom", "Prénom", "Date de naissance", "Elo"]]
    if player_ids is not None:
        players_json = slim_json_dict_by_ids(players_json, player_ids)

    for key, value in players_json.items():
        returned_list.append(
            [
                key,
                value["last_name"],
                value["first_name"],
                f"{json_date_to_str(value["birth_date"])}",
                value["elo"],
            ]
        )

    return returned_list


def list_players_from_tournament(tournament_id: str) -> tuple[str, str, str, str, int]:
    tournaments_json = chess.model.storage.load_data()[chess.model.storage.TOURNAMENTS]

    try:
        player_score = tournaments_json[tournament_id]["players"]
    except KeyError:
        print(
            "L'ID de tournoi n'existe pas. Les IDs qui fonctionnent sont "
            f"{", ".join(tournaments_json.keys())}."
        )
        return [["Tournoi"], ["non trouvé."]]

    player_ids = [x[0] for x in player_score]

    return list_players(player_ids)


def list_rounds_from_tournament(
    tournament_id: str, match_is_int: bool = True
) -> tuple[int, str, str, str, str]:  # multiline if match_is_int is False
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
    rounds_json = slim_json_dict_by_ids(rounds_json, [str(r) for r in rounds])

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
                    f"{"[W]" if match_json["white"] == match_json["score"][0][0] else ""}: "
                    f"{match_json["score"][0][1]}, "
                    f"{str(match_json["score"][1][0])}"
                    f"{"[W]" if match_json["white"] == match_json["score"][1][0] else ""}: "
                    f"{match_json["score"][1][1]}"
                )
                matches_str.append(f"------ {str(match_id)} ------\n{match_result}")

            matches_str = "\n".join(matches_str)

        returned_list.append(
            [
                key,
                value["name"],
                matches_str,
                f"{json_datetime_to_str(value["start_time"])}",
                f"{json_datetime_to_str(value["end_time"])}",
            ]
        )
    return returned_list


def list_matches_from_round(round_id: str):
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
    matches_json = slim_json_dict_by_ids(matches_json, [str(m) for m in match_ids])

    for key, value in matches_json.items():
        returned_list.append(
            [
                key,
                f"{nested_list_to_str(value["score"],": "," vs ")}",
                value["white"],
            ]
        )

    return returned_list


def list_tournaments(
    tournament_id: str = None,
) -> tuple[str, str, str, str, str, str, str, str, str]:  # all tournaments if None
    tournaments_json = chess.model.storage.sort_data()[chess.model.storage.TOURNAMENTS]

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
                f"{nested_list_to_str(value["players"])}",
                f"{"\n".join([str(x) for x in value["rounds"]])}",
                f"{str(chess.model.Address.from_json(value["localization"]))}",
                value["rounds_amount"],
                value["description"],
                f"{json_datetime_to_str(value["start_time"])}",
                f"{json_datetime_to_str(value["end_time"])}",
            ]
        )

    return returned_list


def update_tournament_scores(
    tournament: chess.model.Tournament, finished_matches: list[chess.model.Match]
):
    for match in finished_matches:
        for player in match.players:
            for t_player in tournament.players:
                if t_player[0].id == player.id:
                    t_player[1] += match.score[player]
                    break
    tournament.save()


def start_new_round(tournament: chess.model.Tournament) -> chess.model.Round:
    generated_pairs = generate_pairs_for_new_round(tournament)
    matches = []
    for opponents in generated_pairs:
        match_id = chess.model.generate.generate_available_id(
            chess.model.storage.MATCHES
        )
        matches.append(chess.model.Match(id=match_id, players=opponents))

    round_id = chess.model.generate.generate_available_id(chess.model.storage.ROUNDS)
    new_round = chess.model.Round(
        id=round_id,
        name=f"Round {len(tournament.rounds)+1}",
        matches=matches,
    )
    tournament.rounds.append(new_round)
    return new_round


def generate_pairs_for_new_round(  # FIXME move ? rien à faire ici ?
    tournament: chess.model.Tournament,
) -> list[list[chess.model.Player]]:
    # sort by player score
    sorted_players: list = sorted(tournament.players, key=lambda i: i[1], reverse=True)
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

                # if no more players available, get 1st one given (closest score)
                try:
                    sorted_players[player2_idx]
                except IndexError:
                    player2_idx = 1
                    break

        duos.append([sorted_players[player1_idx][0], sorted_players[player2_idx][0]])
        sorted_players.pop(player2_idx)
        sorted_players.pop(player1_idx)

    return duos


def nested_list_to_str(
    nested_list: list[list[str]], inner_join_str: str = " ", outer_join_str: str = "\n"
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


def json_datetime_to_str(json_datetime: str) -> str:
    if json_datetime is None:
        return "None"
    else:
        return datetime.fromisoformat(json_datetime).strftime("%d-%m-%Y %H:%M")


def slim_json_dict_by_ids(dict_to_slim: dict[str, dict], ids: list) -> dict[str, dict]:
    reduced_dict = {}
    for id in ids:
        try:
            reduced_dict[id] = dict_to_slim[id]
        except KeyError:
            print(f"{id} non trouvé.")
    return reduced_dict
