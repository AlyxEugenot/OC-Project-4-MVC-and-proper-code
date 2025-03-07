import chess.model


def add_player_to_tournament(
    player_id: str, tournament: chess.model.Tournament
) -> chess.model.Player | None:
    player = chess.model.player_from_id(player_id)
    if player is not None:
        tournament.add_player(player)
        chess.model.save_tournament(tournament)
        return player
    else:
        return None
