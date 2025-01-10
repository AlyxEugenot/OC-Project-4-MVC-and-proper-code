import view
import model

class PlayerManager:
    def ask_for_player(self):
        player_id = view.ask_prompt("What is the ID of the player?")

        # if player doesn't exist yet
        if model.player_from_id(player_id) is None:
            self.create_player(player_id)

    def create_player(self, id: str) -> model.Player:
        player = model.Player(
            id=id,
            first_name=view.ask_prompt("First name: "),
            last_name=view.ask_prompt("Last name: "),
            birth_date=view.ask_prompt_date("Birth date (format DD/MM/YYYY): "),
            elo=view.ask_prompt("Elo: "),
        )
        model.storage.save_data(model.storage.player_to_json(player))
        return player
