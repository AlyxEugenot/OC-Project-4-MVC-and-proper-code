from chess.controller.menus._menu import Menu, Choice
import chess.model as model
import chess.generate as generate

m_find_tournament = "find"
m_create_tournament = "create"
m_add_player_to_tournament="add player"


class CreateTournamentMenu(Menu):
    def __init__(self, previous_menu):
        title = "Tournoi"
        texts = {
            m_find_tournament: {
                "Quel est l'ID du tournoi ?",
                Choice(1, "Entrez l'ID :", lambda: self.ask_for_tournament),
            },
            m_create_tournament: {""},
            m_add_player_to_tournament:{""}
        }

        super().__init__(previous_menu, title, texts)

    def ask_for_tournament(self):
        tournament_id = self.view.inputs(
            "What is the ID of the tournament?(can be empty)"
        )

        if model.storage.tournament_from_id(tournament_id) is None:
            self.create_tournament(tournament_id)

    def create_tournament(self, tournament_id: int) -> model.Tournament:
        if generate.is_empty_string(tournament_id):
            tournament_id = generate.generate_specific_str("nnnnnn")
            while model.storage.tournament_from_id(tournament_id) is not None:
                tournament_id = generate.generate_specific_str("nnnnnn")
        name = self.view.ask_prompt("Tournament name: ")
        players: str = self.view.ask_prompt(
            "Enter players' ID separated by commas:(can be empty) "
        )
        players = players.split(",")
        players = [
            player.strip()
            for player in players
            if model.storage.player_from_id(player.strip()) is not None
        ]
        localization = self.view.ask_address("Tournament address: ")
        rounds_amount = self.view.ask_prompt("Rounds amount:(can be empty) ")
        description = self.view.ask_prompt("Description:(can be empty) ")

        tournament = model.Tournament(
            id=tournament_id,
            name=name,
            players=players,
            localization=localization,
        )
        if rounds_amount != "":
            tournament.rounds_amount = rounds_amount
        if description != "":
            tournament.description = description
        model.storage.save_data(model.storage.tournament_to_json(tournament))
        return tournament

    def add_player_to_tournament(self, tournament: model.Tournament):
        player = self.view.ask_player("Player ID to add to tournament: ")
        
        # verify player exists

        tournament.add_player(player)
        model.storage.save_data(model.storage.tournament_to_json(tournament))
