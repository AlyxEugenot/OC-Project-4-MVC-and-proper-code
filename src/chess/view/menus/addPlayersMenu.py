import chess.view
import chess.view.menus._abstract as _abstract
import chess.model as model
import chess.model.generate as generate
import datetime


# TODO mettre tout ce qui touche au model dans le model (donc les générations
# de joueur et les connect ensuite)
class AddPlayers(_abstract.Menu):
    def __init__(self):
        menu_option_name = "Ajouter de nouveaux joueurs"
        title = "Ajout de joueurs"
        super().__init__(title, menu_option_name)
        self.add_child(
            _abstract.Action(
                "Générer des nouveaux joueurs aléatoires", self.generate_new_random
            )
        )
        self.add_child(
            _abstract.Action("Entrer un nouveau joueur", self.generate_new_player)
        )

    def generate_new_random(self):
        amount = int(input("Combien : ").strip())
        players = generate.generate_players(amount)
        for player in players:
            model.save_player(player)
            print(f"player {str(player)} added.")

    def generate_new_player(self):
        player = model.Player(
            id=self.get_valid_player_id(),
            first_name=input("First name : "),
            last_name=input("Last name : "),
            birth_date=self.get_valid_date(),
            elo=int(input("Elo : ").strip()),
        )
        model.save_player(player)
        print(f"player {str(player)} added.")

    def get_valid_player_id(self) -> str:  # FIXME put in model
        player_id = input("Player ID : ")
        if not model.Player(player_id, "", "", None).is_id_valid():
            print("ID is not valid (format AB12345).")
            player_id = self.get_valid_player_id()
        if model.player_from_id(player_id) is not None:
            print("ID already exists.")
            player_id = self.get_valid_player_id()
        return player_id

    def get_valid_date(self) -> datetime.date:  # FIXME put in model
        try:
            date = input("Birth date (format DD/MM/YYYY) : ")
            day, month, year = [int(x.strip()) for x in date.split("/")]    
            date = datetime.date(year, month, day)
        except ValueError:  # TODO put good kind of error here
            print("Wrong date format.")
            date = self.get_valid_date()
        return date