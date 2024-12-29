"""Docstring to come"""

import view
import models.model as model
import models.saving_data
import generate


class Controller:

    # créer un joueur
    def ask_for_player(self):
        user_input = view.ask_prompt("What is the ID of the player?")

        # if player already exists
        if self.find_player(id) is None:
            self.create_player(id)

    def find_player(self, id: str) -> model.Player:
        data = models.saving_data.load_data()
        if id in data[models.saving_data.PLAYERS]:
            return data[models.saving_data.PLAYERS][
                id
            ]  # FIXME Get saved objects into Player object
        else:
            return None

    def create_player(self, id: str) -> model.Player:
        player = model.Player(
            id=id,
            first_name=view.ask_prompt("First name: "),
            last_name=view.ask_prompt("Last name: "),
            birth_date=view.ask_prompt_date("Birth date (format DD/MM/YYYY): "),
            elo=view.ask_prompt("Elo: "),
        )

        return player

    # ajouter un joueur à un tournoi

    # créer/lancer un tournoi
    # créer/lancer un round
    # "créer" un match
