from controllers.app import AppController
from datetime import datetime
from time import strftime

class Views:
    @staticmethod
    def create_tournament_view():
        players = []
        tournament_info = {}
        
        print("Vous devez renseigner les informations suivantes:")
        print("Nom du tournoi:")
        tournament_info["name"] = input()
        print("Lieu:")
        tournament_info["location"] = input()
        print("Commentaires:")
        tournament_info["description"] = input()
        print("nombre de tours:")
        tournament_info["nb_rounds"] = input()
        print("Joueurs participant:")
        while True:
            player = int(input())
            players.append(player)
            if len(players) == 8:
                tournament_info["players"] = players
                break
            else:
                pass
        print("Quels types de parties seront jouées?")
        print("bullet, blitz, coup rapide")
        tournament_info["rounds"] = []
        tournament_info["nb_of_played_round"] = 0
        tournament_info["game_rules"] = input()
        tournament_info["date"] = str(datetime.now())
        AppController.create_tournament(tournament_info)

    @staticmethod
    def create_player_view():
        player_info = {}
        print("Vous devez renseigner les informations suivantes:")
        print("Prénom:")
        player_info["firstname"] = input()
        print("Nom")
        player_info["lastname"] = input()
        print("Date de naissance:")
        player_info["birth_date"] = input()
        print("Genre:")
        player_info["gender"] = input()
        print("Classement")
        player_info["elo"] = int(input())
        AppController.create_player(player_info)

    @staticmethod
    def enter_results_view():
        pass

    @staticmethod
    def show_generated_round(round):
        if round:
            print(round['games'])
            return
        print('Pas de round généré.')

    @staticmethod
    def tournament_choice_view():
        tournament_list = AppController.get_tournament_list()
        print(tournament_list)
        for tournament in tournament_list.items:
            print(f"id: {tournament.id.value}, name: {tournament.name.value}")
        print("Quel tournoi cela concerne-t-il?")
        tournament_id_user_choice = input()
        return tournament_id_user_choice

    @staticmethod
    def generate_round_view():
        tournament_id_user_choice = int(Views.tournament_choice_view())
        round = AppController.generate_tour(tournament_id_user_choice)
        Views.show_generated_round(round)

    @staticmethod
    def get_match_id_view(games_list):
        if not games_list:
            print("La liste des matchs est vide.")
            return
        for game in games_list.items:
            print(f"{game.match_id.value}: {game.joueur1.value} vs {game.joueur2.value}")
        match_id_user_choice = input()
        return match_id_user_choice

    @staticmethod
    def get_round_results_view():
        tournament_id_user_choice = int(Views.tournament_choice_view())
        games_list, round_id = AppController.get_game_list(tournament_id_user_choice)
        if not games_list:
            print("Pas de matchs trouvé")
            return
        matchs_results = []
        while True:
            match_id_user_choice = Views.get_match_id_view(games_list)
            if match_id_user_choice.upper() == "Q":
                # print(matchs_results)
                # AppController.set_tour_results(matchs_results, round_id, tournament_id_user_choice,
                #                                 match_id, player_one_score, player_two_score)
                break
            match_id, player_one_score, player_two_score = list(map(float,
                                                            match_id_user_choice.split(" ")))

            AppController.set_tour_results(matchs_results, round_id, tournament_id_user_choice,
                                           match_id, player_one_score, player_two_score)

    @staticmethod
    def show_provisional_ranking():
        tournament_id_user_choice = int(Views.tournament_choice_view())
        players = AppController.get_provisional_ranking(tournament_id_user_choice)
        for player in players:
            print(f"Prénom: {player.firstname.value}"
                  f"| score tournoi: {player.tournament_score}"
                  f"| elo: {player.elo.value}")

    @staticmethod
    def player_choice_view():
        # tournament_id_user_choice = Views.tournament_choice_view()
        players = AppController.get_player_info()
        for player in players:
            print(player["firstname"])
        print("Quel est le joueur qui vous intéresse?")
        player_choice = input()
        if player_choice in [player["firstname"] for player in players]:
            return player_choice
            
        print("Votre demande ne correspond pas aux joueurs demandés...")

    @staticmethod
    def get_player_info_view():
        player = Views.player_choice_view()
        print(AppController.get_player_info(player))
        return

    @staticmethod
    def set_new_elo_view():
        player = Views.player_choice_view()
        while True:
            print("Quel est le nouvel elo du joueur?")
            new_elo = int(input())
            if new_elo >= 0:
                AppController.set_player_elo(player, new_elo)
                break
            print("La valeur rentrée n'est pas correcte.")
