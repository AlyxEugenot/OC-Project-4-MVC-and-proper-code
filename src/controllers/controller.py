"""Docstring to come"""  # TODO

import view
import models.model as model
import models.saving_data
import generate


class Controller:

    # créer un joueur
    def ask_for_player(self):
        player_id = view.ask_prompt("What is the ID of the player?")

        # if player doesn't exist yet
        if models.saving_data.player_from_id(player_id) is None:
            self.create_player(player_id)

    def create_player(self, id: str) -> model.Player:
        player = model.Player(
            id=id,
            first_name=view.ask_prompt("First name: "),
            last_name=view.ask_prompt("Last name: "),
            birth_date=view.ask_prompt_date("Birth date (format DD/MM/YYYY): "),
            elo=view.ask_prompt("Elo: "),
        )
        models.saving_data.save_data(models.saving_data.player_to_json(player))
        return player

    def ask_for_tournament(self):
        tournament_id = view.ask_prompt(
            "What is the ID of the tournament?(can be empty)"
        )

        if models.saving_data.tournament_from_id(tournament_id) is None:
            self.create_tournament(tournament_id)

    def create_tournament(self, tournament_id: int) -> model.Tournament:
        if generate.is_empty_string(tournament_id):
            tournament_id = generate.generate_specific_str("nnnnnn")
            while models.saving_data.tournament_from_id(tournament_id) is not None:
                tournament_id = generate.generate_specific_str("nnnnnn")
        name = view.ask_prompt("Tournament name: ")
        players = view.ask_prompt(
            "Enter players' ID separated by commas:(can be empty) "
        )
        players = players.split(",")
        players = [
            player.strip()
            for player in players
            if models.saving_data.player_from_id(player.strip()) is not None
        ]
        localization = self.ask_address("Tournament address:(can be empty) ")
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

        models.saving_data.tournament_to_json(tournament)
        return tournament

    # ajouter un joueur à un tournoi

    def ask_address(self, intro: str) -> model.Address:
        view.intro(intro)

        addressee_id = view.ask_prompt("Addressee ID:(generate all if 'gen' is typed) ")
        if addressee_id == "gen":
            return generate.generate_address()
        delivery_point = view.ask_prompt("delivery_point: ")
        additional_geo_info = view.ask_prompt("additional_geo_info:(can be empty) ")
        house_nb_street_name = view.ask_prompt("house_nb_street_name: ")
        additional_delivery_info = view.ask_prompt(
            "additional_delivery_info:(can be empty) "
        )
        postcode = view.ask_prompt("postcode: ")
        country_name = view.ask_prompt("country_name:(can be empty) ")

        address = model.Address(
            addressee_id=addressee_id,
            delivery_point=delivery_point,
            house_nb_street_name=house_nb_street_name,
            postcode=postcode,
        )
        if additional_geo_info != "":
            address.additional_geo_info = additional_geo_info
        if additional_delivery_info != "":
            address.additional_delivery_info = additional_delivery_info
        if country_name != "":
            address.country_name = country_name

        return address

    # créer/lancer un tournoi
    # créer/lancer un round
    # "créer" un match
