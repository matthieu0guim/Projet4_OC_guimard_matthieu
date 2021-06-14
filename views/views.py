

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
    def tournament_choice_view(tournament_list, generate_round=False, checking_ranking=False):
        for tournament in tournament_list.items:
            print(f"id: {tournament.id.value}, name: {tournament.name.value}")
        if not generate_round and not checking_ranking:
            print("Pour quel tournoi voulez-vous rentrer les résultats?")
            tournament_id_user_choice = input()
            return tournament_id_user_choice
        elif not generate_round and checking_ranking:
            print('Quel tournoi vous intéresse?')
            tournament_id_user_choice = input()
            return tournament_id_user_choice
        print("Pour quel tournoi voulez-vous générer un round?\n")
        tournament_id_user_choice = input()
        return tournament_id_user_choice

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
    def get_round_results_view(match_id_user_choice):
        match_id, player_one_score, player_two_score = list(map(float,
                                                            match_id_user_choice.split(" ")))
        return match_id, player_one_score, player_two_score

    @staticmethod
    def show_provisional_ranking(players):
        for player in players:
            print(f"Prénom: {player.firstname.value}"
                  f"| score tournoi: {player.tournament_score}"
                  f"| elo: {player.elo.value}")

    @staticmethod
    def player_choice_view(players):
        while True:
            for player in players:
                print(player['firstname'])
            print("Quel est le joueur qui vous intéresse?")
            player_choice = input()
            if player_choice in [player['firstname'] for player in players]:
                return player_choice
            print("Votre demande ne correspond pas aux joueurs demandés...")

    @staticmethod
    def get_player_info_view(player_info):
        print(player_info)
        return

    @staticmethod
    def get_new_elo_view(player_choice):
        while True:
            print("Quel est le nouvel elo du joueur?")
            new_elo = int(input())
            if new_elo >= 0:
                return new_elo
            print("La valeur rentrée n'est pas correcte.")
