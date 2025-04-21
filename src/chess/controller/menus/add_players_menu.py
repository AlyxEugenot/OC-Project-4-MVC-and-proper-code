"""Menu for adding players to data.json. Possibly random."""

from chess.controller.menus import _abstract
from chess import model
from chess.model import generate, storage


class AddPlayers(_abstract.Menu):
    """Menu for adding players to data.json.

    Inherit from Menu.

    Children:
        generate_new_random
        generate_new_player
    """

    def __init__(self):
        """Initialize super init.

        Add children:
            generate_new_random
            generate_new_player
        """
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
        self.add_child(
            _abstract.Action(
                "Afficher les joueurs existants.",
                lambda: self.display_report(self.reports.all_players),
            )
        )

    def generate_new_random(self):
        """Add new random players to data.json.

        Number of generated players from user input.
        """
        amount = int(self.view.my_input("Combien : ").strip())
        players = generate.generate_players(amount)
        for player in players:
            player.save()
            self.view.my_print(f"player {str(player)} added.")

    def generate_new_player(self):
        """Add new player from user input to data.json."""
        player_id = self.view.my_input("ID du joueur : ")
        while not storage.is_id_valid(player_id, storage.PLAYERS):
            player_id = self.view.my_input("ID du joueur : ")

        player = model.Player(
            _id=player_id,
            first_name=self.view.my_input("First name : "),
            last_name=self.view.my_input("Last name : "),
            birth_date=self.view.get_valid_date(),
            elo=int(self.view.my_input("Elo : ")),
        )
        player.save()
        self.view.my_print(f"player {str(player)} added.")
