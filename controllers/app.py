from db.models import Tournament, Player


class AppController:
    _current_tournament = None

    @classmethod
    def create_tournament(cls, attrs):
        id = Tournament.set_tournament_id()
        attrs["id"] = id
        Tournament.create(attrs)
    
    @classmethod
    def set_tournament_players(cls, tournament_id_user_choice, players):
        Tournament.set_tournament_nb_of_round(players, tournament_id_user_choice)
            # TODO faire une vue pour créer le tournoi

    @classmethod
    def create_player(cls, attrs):
        Player.create(attrs)
# TODO faire une view pour créer un joueur
    @classmethod
    def generate_tour(cls, tournament_id_user_choice):
        round = Tournament.generate_round(tournament_id_user_choice)
        return round

    @classmethod
    def set_tour_results(cls, matchs_results, round_id, tournament_id_user_choice,
                         match_id, player_one_score=None, player_two_score=None):
        
        Tournament.enter_results(tournament_id_user_choice, round_id,
                                    match_id, player_one_score,
                                    player_two_score, matchs_results)
        Tournament.save_results(matchs_results, round_id, tournament_id_user_choice)


    @classmethod
    def get_provisional_ranking(cls, tournament_id_user_choice):
        players = Tournament.get_players(tournament_id_user_choice)
        return players

    @classmethod
    def get_player_info(cls, tournament_id_user_choice, player_choice=None):
        if not player_choice:
            players = Tournament.get_players(int(tournament_id_user_choice))
            return players
        player_info = Tournament.get_player_info(player_choice)
        return player_info
        

    @classmethod
    def set_player_elo(cls):
        players = Tournament.get_all_players()
        player_choice = Views.player_choice_view(players)
        player_info = Tournament.get_player_info(player_choice)
        Views.get_player_info_view(player_info)
        Tournament.change_player_elo(player_choice, Views.get_new_elo_view(player_choice))

    @classmethod
    def get_tournament_list(cls):
        tournament_list = Tournament.get_tournament_list()
        return tournament_list

    @classmethod
    def get_game_list(cls, tournament_id):
        return Tournament.get_game_list(tournament_id)