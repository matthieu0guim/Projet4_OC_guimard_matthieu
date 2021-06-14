from db.models import Tournament, Player
from views.views import Views


class AppController:
    _current_tournament = None

    @classmethod
    def create_tournament(cls, attrs):
        id = Tournament.set_tournament_id()
        attrs["id"] = id
        Tournament.create(attrs)
# TODO faire une vue pour créer le tournoi
    @classmethod
    def create_player(cls, attrs):
        Player.create(attrs)
# TODO faire une view pour créer un joueur
    @classmethod
    def generate_tour(cls):
        tournament_list = Tournament.get_tournament_list()
        tournament_id_user_choice = int(
            Views.tournament_choice_view(tournament_list, generate_round=True))
        round = Tournament.generate_round(tournament_id_user_choice)
        return Views.show_generated_round(round)

    @classmethod
    def set_tour_results(cls):
        tournament_list = Tournament.get_tournament_list()
        tournament_id_user_choice = int(Views.tournament_choice_view(tournament_list))
        games_list, round_id = Tournament.get_game_list(tournament_id_user_choice)
        if not games_list:
            print("Pas de matchs trouvé")
            return
        matchs_results = []
        while True:
            match_id_user_choice = Views.get_match_id_view(games_list)
            if match_id_user_choice == "q" or match_id_user_choice == "Q":
                print(matchs_results)
                Tournament.save_results(matchs_results, round_id, tournament_id_user_choice)
                break
            match_id_user_choice, player_one_score, player_two_score = Views.get_round_results_view(
                match_id_user_choice)
            print(tournament_id_user_choice, round_id,
                                     match_id_user_choice, player_one_score,
                                     player_two_score, matchs_results )
            Tournament.enter_results(tournament_id_user_choice, round_id,
                                     match_id_user_choice, player_one_score,
                                     player_two_score, matchs_results)

    @classmethod
    def get_provisional_ranking(cls):
        tournament_list = Tournament.get_tournament_list()
        tournament_id_user_choice = int(Views.tournament_choice_view(
            tournament_list, checking_ranking=True))
        players = Tournament.get_players(tournament_id_user_choice)
        Views.show_provisional_ranking(players)

    @classmethod
    def get_player_info(cls):
        tournament_list = Tournament.get_tournament_list()
        tournament_id_user_choice = Views.tournament_choice_view(
            tournament_list, checking_ranking=True)
        players = Tournament.get_players(int(tournament_id_user_choice))
        player_choice = Views.player_choice_view(players)
        player_info = Tournament.get_player_info(player_choice)
        Views.get_player_info_view(player_info)
        return

    @classmethod
    def set_player_elo(cls):
        players = Tournament.get_all_players()
        player_choice = Views.player_choice_view(players)
        player_info = Tournament.get_player_info(player_choice)
        Views.get_player_info_view(player_info)
        Tournament.change_player_elo(player_choice, Views.get_new_elo_view(player_choice))
