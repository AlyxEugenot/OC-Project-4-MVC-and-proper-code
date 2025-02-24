import chess.view
import chess.view.menus._abstract as _abstract
import chess.model as model
import chess.model.generate as generate


class Reports(_abstract.Menu):
    def __init__(self):
        title = "Rapports"
        menu_option_name = "Afficher les rapports"
        super().__init__(title=title, menu_option_name=menu_option_name)
        self.add_child(_abstract.Action("Liste de tous les joueurs",self.all_players))
        self.add_child(_abstract.Action("Liste de tous les tournois",self.all_tournaments))
        self.add_child(_abstract.Action("Liste de tous les joueurs d'un tournoi",self.all_players_from_tournament))
        self.add_child(_abstract.Action("Liste de tous les rounds d'un tournoi et tous ses matchs",self.all_rounds_of_tournament_and_all_their_matches))
        self.add_child(_abstract.Action("Liste de tous les rounds d'un tournoi",self.all_rounds_of_tournament))
        self.add_child(_abstract.Action("Liste de tous les matchs d'un round",self.all_matches_of_round))

    def all_players(self):
        print("Liste de tous les joueurs") # sort les joueurs
    def all_tournaments(self):
        print("all_tournaments")
    def all_players_from_tournament(self):
        print("all_players_from_tournament")
    def all_rounds_of_tournament_and_all_their_matches(self):
        print("all_rounds_of_tournament_and_all_their_matches")
    def all_rounds_of_tournament(self):
        print("all_rounds_of_tournament")
    def all_matches_of_round(self):
        print("all_matches_of_round")

