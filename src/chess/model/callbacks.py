import chess.model
import chess.model.storage
import chess.model.generate
from datetime import date


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


def list_all_players() -> list[str, str, str, date, int]:
    players_json = chess.model.storage.sort_data()[chess.model.storage.PLAYERS]

    returned_list = [["ID", "Nom", "Prénom", "Date de naissance", "Elo"]]
    for key, value in players_json.items():
        returned_list.append(
            [
                key,
                value["last_name"],
                value["first_name"],
                value["birth_date"],
                value["elo"],
            ]
        )

    return returned_list


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
        if len(sorted_players) // 2 > 2:
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

