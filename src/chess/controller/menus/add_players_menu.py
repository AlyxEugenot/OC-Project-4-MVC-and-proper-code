"""Menu for adding players to data.json. Possibly random."""

from chess.controller.menus import _abstract
from chess import model
from chess.model import generate, storage
from chess.utils import utils


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
        amount = utils.input_int("Combien : ", self.view)
        players = generate.generate_players(amount)
        for player in players:
            player.save()
            self.view.my_print(f"player {str(player)} added.")

    def generate_new_player(self):
        """Add new player from user input to data.json."""
        player_id = self.input_player_id()

        first_name = self.view.my_input("Prénom : ", can_be_empty=False)
        last_name = self.view.my_input("Nom : ", can_be_empty=False)
        birth_date = self.view.get_valid_date()
        elo = utils.input_int("Elo : ", self.view)

        player = model.Player(
            _id=player_id,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            elo=elo,
        )
        player.save()
        self.view.my_print(f"Joueur {str(player)} ajouté.")

    def input_player_id(self) -> str:
        """Get user to input available player id.

        Returns:
            str: Player ID.
        """
        player_id_is_ok = False
        problem = ""
        while not player_id_is_ok:
            if problem != "":
                self.view.my_print(f"\n{problem}\n")

            player_id = self.view.my_input(
                "Quel est l'ID du joueur ? (Généré au hasard si vide) "
            )
            if player_id == "":
                player_id = generate.generate_available_id(storage.PLAYERS)
                break

            (player_id_is_ok, problem) = storage.is_id_valid(
                player_id, storage.PLAYERS
            )
        return str(player_id)
