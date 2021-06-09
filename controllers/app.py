from db.models import Tournament, Player, Match, Round
from views.views import Views

class AppController:
    _current_tournament = None
    
    @classmethod
    def create_tournament(cls, attrs):
        Tournament.create(attrs)
        
    @classmethod
    def create_player(cls, attrs):
        Player.create(attrs)
    
    @classmethod
    def generate_tour(cls):
        tournament_list = Tournament.get_tournament_list()
        tournament_id_user_choice = int(Views.tournament_choice_view(tournament_list, generate_round=True))
        round = Tournament.generate_round(tournament_id_user_choice)
        return Views.show_generated_round(round)
    
    @classmethod
    def set_tour_results(cls):
        tournament_list = Tournament.get_tournament_list()
        tournament_id_user_choice = int(Views.tournament_choice_view(tournament_list))
        games_list, round_id = Tournament.get_game_list(tournament_id_user_choice)
        matchs_results = []
        while True:
            match_id_user_choice = Views.get_match_id_view(games_list)
            if match_id_user_choice == "q" or match_id_user_choice == "Q":
                Tournament.save_results(matchs_results, round_id, tournament_id_user_choice)
                break
            match_id_user_choice, player_one_score, player_two_score = Views.get_round_results_view(match_id_user_choice)
            
            Tournament.enter_results(tournament_id_user_choice, round_id, match_id_user_choice, player_one_score, player_two_score, matchs_results)
            
    @classmethod
    def get_provisional_ranking(cls):
        tournament_list = Tournament.get_tournament_list()
        tournament_id_user_choice = int(Views.tournament_choice_view(tournament_list, checking_ranking=True))
        players = Tournament.get_players(tournament_id_user_choice)
        Views.show_provisional_ranking(players)

    
    @classmethod
    def get_player_info(cls):
        pass
    
    @classmethod
    def set_player_rank(cls):
        pass
    
    @classmethod
    def set_current_tournament(cls):
        pass
    
    @classmethod
    def unset_current_tournament(cls):
        pass