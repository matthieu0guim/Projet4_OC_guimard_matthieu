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
        tournament_id = int(Views.generate_round_view())
        round = Tournament.generate_round(tournament_id)
        return Views.show_generated_round(round)
    
    @classmethod
    def set_tour_results(cls):
        tournament_list = Tournament.get_tournament_list()
        tournament_id_user_choice = Views.enter_results_view(tournament_list)
        

    
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