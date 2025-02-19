from chess.controller.menus._menu import Menu, TextItem
import chess.model as model
import chess.generate as generate

t_find_tournament = "find"
m_create_tournament = "create"
m_add_player_to_tournament = "add player"


class CreateTournamentMenu(Menu):
    def __init__(self, previous_menu):
        title = "Tournoi"
        self.tournament = None
        texts = {
            t_find_tournament: {
                "Quel est l'ID du tournoi ? (generate random if empty) ",
                None,
            },
            m_create_tournament: {""},
            m_add_player_to_tournament: {""},
        }

        super().__init__(
            previous_menu=previous_menu,
            title=title,
            text_items=texts,
            loop_item_by_default=False,
        )

    def work(self) -> model.Tournament:
        tournament_id = self.view.input(self.text_items[t_find_tournament].text)

        if model.storage.tournament_from_id(tournament_id) is not None:
            # TODO confirmation de "on a trouvé un tournoi à tel ID, voulez-vous en créer un avec un ID différent ?"
            return model.storage.tournament_from_id(tournament_id)

        return self.create_tournament(tournament_id)

    def create_tournament(self, tournament_id: str) -> model.Tournament:
        if generate.is_empty_string(tournament_id):
            tournament_id = generate.generate_specific_str("nnnnnn")
            while model.storage.tournament_from_id(tournament_id) is not None:
                tournament_id = generate.generate_specific_str("nnnnnn")
        name = self.view.input("Tournament name: ")
        players: str = self.view.input(
            "Enter players' ID separated by commas:(can be empty) "
        )
        players = players.split(",")
        players_found = [
            player.strip()
            for player in players
            if model.storage.player_from_id(player.strip()) is not None
        ]
        localization = self.view.create_address("\nTournament address: ")
        # TODO find avant
        # TODO faire le find address
        # TODO faire un menu pour les create address et player auquel au switch quand besoin ?
        rounds_amount = self.view.input("\nRounds amount: ", "4")
        description = self.view.input("Description:(generate if empty) ")

        tournament = model.Tournament(
            id=tournament_id,
            name=name,
            players=players_found,
            localization=localization,
        )
        if rounds_amount != "":
            tournament.rounds_amount = rounds_amount
        if description != "":
            tournament.description = description
        model.storage.save_data(model.storage.tournament_to_json(tournament))
        return tournament

    def add_player_to_tournament(
        self, tournament: model.Tournament
    ):  # FIXME pas utilisé
        player_id = self.view.input("Player ID to add to tournament: ")

        player = model.player_from_id(player_id)
        # verify player exists
        if player is None:
            player = generate.generate_players(1)[0]
            print(f"player not found, {player} generated instead")
            # player = self.view.create_player() #TODO

        tournament.add_player(player)
        model.storage.save_data(model.storage.tournament_to_json(tournament))
