import chess.controller.menus._abstract as _abstract
import chess.model as model
import chess.utils as utils
import datetime


class AddPlayers(_abstract.Menu):
    def __init__(self):
        menu_option_name = "Ajouter de nouveaux joueurs"
        title = "Ajout de joueurs"
        super().__init__(title=title, menu_option_name=menu_option_name)
        self.add_child(
            _abstract.Action(
                "Générer des nouveaux joueurs aléatoires",
                self.generate_new_random,
            )
        )
        self.add_child(
            _abstract.Action(
                "Entrer un nouveau joueur", self.generate_new_player
            )
        )

    def generate_new_random(self):
        amount = int(self.view.my_input("Combien : ").strip())
        players = utils.generate_players(amount)
        for player in players:
            player.save()
            self.view.my_print(f"player {str(player)} added.")

    def generate_new_player(self):
        player = model.Player(
            id=self.get_valid_player_id(),
            first_name=self.view.my_input("First name : "),
            last_name=self.view.my_input("Last name : "),
            birth_date=self.get_valid_date(),
            elo=int(self.view.my_input("Elo : ").strip()),
        )
        player.save()
        self.view.my_print(f"player {str(player)} added.")

    def get_valid_player_id(self) -> str:
        player_id = self.view.my_input("Player ID : ")
        if not model.Player(player_id, "", "", None).is_id_valid():
            self.view.my_print("ID is not valid (format AB12345).")
            player_id = self.get_valid_player_id()
        if model.Player.from_id(player_id) is not None:
            self.view.my_print("ID already exists.")
            player_id = self.get_valid_player_id()
        return player_id

    def get_valid_date(self) -> datetime.date:
        try:
            date = self.view.my_input("Birth date (format DD/MM/YYYY) : ")
            day, month, year = [int(x.strip()) for x in date.split("/")]
            date = datetime.date(year, month, day)
        except ValueError:
            self.view.my_print("Wrong date format.")
            date = self.get_valid_date()
        return date
