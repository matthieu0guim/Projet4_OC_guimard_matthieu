from db.models import Tournament


class Views:

    def enter_results_view():
        pass
    
    
    # @staticmethod
    # def generate_round_view():
    #     print(f"Pour quel tournoi voulez-vous générer un round? \n ")
    #     tournament_id = input()
    #     return tournament_id
    
    @staticmethod
    def show_generated_round(round):
        print(round[0]['games'])

    @staticmethod
    def tournament_choice_view(tournament_list, generate_round=False, checking_ranking=False):
        if not generate_round and not checking_ranking:
            print(f"Pour quel tournoi voulez-vous rentrer les résultats?")
            for tournament in tournament_list.items:
                print(f"id: {tournament.id.value}, name: {tournament.name.value}")
            tournament_id_user_choice = input()
            return tournament_id_user_choice
        
        elif not generate_round and checking_ranking:
            print('Pour quel tournoi voulez-vous consulter le classement?')
            tournament_id_user_choice = input()
            return tournament_id_user_choice
        
        print(f"Pour quel tournoi voulez-vous générer un round? \n ")
        tournament_id_user_choice = input()
        return tournament_id_user_choice

    @staticmethod
    def get_match_id_view(games_list):
        for game in games_list.items:
            print(f"{game.match_id.value}: {game.joueur1.value} vs {game.joueur2.value}")
        match_id_user_choice = input()
        return match_id_user_choice
        
    @staticmethod
    def get_round_results_view( match_id_user_choice):
        # for game in games_list.items:
        #     print(f"{game.match_id.value}: {game.joueur1.value} vs {game.joueur2.value}")
        # match_id_user_choice = input()
        # if match_id_user_choice == "q" or match_id_user_choice == "Q":
        #     return match_id_user_choice

        match_id, player_one_score, player_two_score = list(map(float, match_id_user_choice.split(" ")))
        return match_id, player_one_score, player_two_score

    @staticmethod
    def show_provisional_ranking(players):
        for player in players:
            print(f"Prénom: {player.firstname.value} | score tournoi: {player.tournament_score} | elo: {player.elo.value}")