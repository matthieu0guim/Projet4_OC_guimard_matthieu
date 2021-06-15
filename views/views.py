from controllers.app import AppController

class Views:

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
        tournament_id_user_choice = Views.tournament_choice_view()
        players = AppController.get_player_info(tournament_id_user_choice)
        # while True:
        
        for player in players:
            print(player.firstname.value)
        print("Quel est le joueur qui vous intéresse?")
        player_choice = input()
        if player_choice in [player.firstname.value for player in players]:
            return tournament_id_user_choice, player_choice
            
        print("Votre demande ne correspond pas aux joueurs demandés...")

    @staticmethod
    def get_player_info_view():
        tournament_id_user_choice, player = Views.player_choice_view()
        print(AppController.get_player_info(tournament_id_user_choice, player))
        return

    @staticmethod
    def get_new_elo_view(player_choice):
        while True:
            print("Quel est le nouvel elo du joueur?")
            new_elo = int(input())
            if new_elo >= 0:
                return new_elo
            print("La valeur rentrée n'est pas correcte.")

    @staticmethod
    def get_tournament_players_view():
        players = []
        tournament_id_user_choice = int(Views.tournament_choice_view())
        while True:
            player = input() # ressenti: un utilisateur ne rentrera jamais l'id d'un joueur mais son nom...
            if player.upper() == "Q":
                if len(players) % 2 != 0:
                    print(f"Il faut un nombre paire de joueur. Veuillez renseigner un autre joueur."
                          f"Pour corriger une erreur, rentrer l'id n°1 et relancez la saisie des joueurs")
                    continue
                break
            players.append(int(player))
        AppController.set_tournament_players(tournament_id_user_choice, players)
        
