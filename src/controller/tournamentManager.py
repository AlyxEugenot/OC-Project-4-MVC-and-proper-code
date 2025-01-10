import view
import model
import generate
import controller

class tournamentManager:
    
    def ask_for_tournament(self):
        tournament_id = view.ask_prompt(
            "What is the ID of the tournament?(can be empty)"
        )

        if model.storage.tournament_from_id(tournament_id) is None:
            self.create_tournament(tournament_id)

    def create_tournament(self, tournament_id: int) -> model.Tournament:
        if generate.is_empty_string(tournament_id):
            tournament_id = generate.generate_specific_str("nnnnnn")
            while model.storage.tournament_from_id(tournament_id) is not None:
                tournament_id = generate.generate_specific_str("nnnnnn")
        name = view.ask_prompt("Tournament name: ")
        players = view.ask_prompt(
            "Enter players' ID separated by commas:(can be empty) "
        )
        players = players.split(",")
        players = [
            player.strip()
            for player in players
            if model.storage.player_from_id(player.strip()) is not None
        ]
        localization = self.ask_address("Tournament address: ")
        rounds_amount = view.ask_prompt("Rounds amount:(can be empty) ")
        description = view.ask_prompt("Description:(can be empty) ")

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
        player = view.ask_player("Player ID to add to tournament: ")
        
        tournament.add_player(player)
        model.storage.save_data(model.storage.tournament_to_json(tournament))
