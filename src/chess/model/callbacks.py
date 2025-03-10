import chess.model
import chess.model.storage
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
