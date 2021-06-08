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
        tournament_id = int(Views.generate_round_view())
        round = Tournament.generate_round(tournament_id)
        return Views.show_generated_round(round)
    
    @classmethod
    def set_tour_results(cls):
        tournament_list = Tournament.get_tournament_list()
        tournament_id_user_choice = Views.enter_results_view(tournament_list)
        games_list = Tournament.get_game_list(tournament_id_user_choice)
        matchs_results = []
        while True:
            match_id = Views.get_round_result_view(games_list, matchs_results)
            if match_id == "q" or match_id == "Q":
                Tournament.save_results(matchs_results, round_id, tournament_id_user_choice)


    
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