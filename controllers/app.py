""""
This module receive user wishes from the view module and call
the correct methods in the model.
"""
from db.models import Tournament, Player

from copy import deepcopy

class AppController:
    
    _current_tournament = None

    @classmethod
    def create_tournament(cls, attrs):
        """Create the tournament in database
        attrs are the attributes collected by the view
        """
        id = Tournament.set_tournament_id()
        attrs["id"] = id
        Tournament.create(attrs)
    
    @classmethod
    def create_player(cls, attrs):
        """Create a new player in database
        attrs are the attributes collected by the view"""
        id = Tournament.set_player_id()
        attrs["id"] = id
        Player.create(attrs)

    @classmethod
    def generate_tour(cls, tournament_id_user_choice):
        """Generate a new round for an ongoing tournament
        The wished tournament is entered with the attribute tournament_id_user_choice
        """
        round = Tournament.generate_round(tournament_id_user_choice)
        return round

    @classmethod
    def set_tour_results(cls, matchs_results, round_id, tournament_id_user_choice,
                         match_id, player_one_score=None, player_two_score=None):
        """Allowes to register a round result
        matchs_results is a list of matches
        round_id is the concerned round
        tournament_id_user_choice is the concerned tournament
        match_id is the id of a match in the round
        player_one_score/player_two_score are the resuls of the match refered by match_id
        """
        Tournament.enter_results(tournament_id_user_choice, round_id,
                                    match_id, player_one_score,
                                    player_two_score, matchs_results)
        Tournament.save_results(matchs_results, round_id, tournament_id_user_choice)

    @classmethod
    def get_provisional_ranking(cls, tournament_id_user_choice):
        """Used to send the ranking of a tournament
        It returns a sorted by tournament_score list for the wished tournament
        """
        players = Tournament.get_players(tournament_id_user_choice)
        return players


    @classmethod
    def get_player_info(cls, player_choice=None):
        """send either informations about every players of the data base
        If the player_choice is not specified, all players in database are returned
        If the player_choice is specified with its id it only returns the concerned one
         """
        if not player_choice:
            players = Tournament.get_all_players()
            return players
        player_info = Tournament.get_player_info(player_choice)
        return player_info
        

    @classmethod
    def set_player_elo(cls, player, new_elo):
        """Allows the user to update a player's elo
        It takes the id of the player and the new value as arguments
        """
        Tournament.change_player_elo(player, new_elo)

    # @classmethod
    # def get_tournament_list(cls):
    #     """Return all tournaments presents in database
    #     It returns the all dictionary about each tournament"""
    #     # tournament_list = Tournament.get_tournament_list()
    #     tournament_list = Tournament.get_all_tournaments()
    #     return tournament_list

    @classmethod
    def get_game_list(cls, tournament_id):
        """Return the games list of the ongoing round for the specified tournament"""
        return Tournament.get_game_list(tournament_id)

    @classmethod
    def get_report(cls, choice=0, tournament_choice=None, sorting=None, round_choice=None, choosing=None):
        """Return informations about a required subject
        5 kind of reports are possible:
                - All players in database sorted alphabetically or by rank
                - The list of all tournaments in database
                - The list of player in a tournament sorted alphabetically or by rank
                - The list of played and ongoing rounds in a tournament
                - The list of games in a round for a specified tournament
        """
        report = []
        returned_report = []
        if choice == 1:
            if sorting == "a":
                report = sorted(Tournament.get_all_players(), key=lambda x: x["firstname"].lower())
            if sorting == "c":
                report = sorted(Tournament.get_all_players(), key=lambda x: x["elo"], reverse=True)
            for value in report:
                returned_report.append([f"Prénom: {value['firstname']}",
                                        f"Nom: {value['lastname']}",
                                        f"Date de naissance: {value['birth_date']}",
                                        f"Classement elo: {value['elo']}"])
        if choice == 2:
            report = Tournament.get_all_tournaments()
            for value in report:
                if choosing:
                    try:
                        del value["lists_of_possible_games"]
                    except KeyError:
                        pass
                    return report
                returned_report.append([f"Nom: {value['name']}",
                                        f"Lieu: {value['location']}",
                                        f"Nombre de tours prévus: {value['nb_rounds']}",
                                        f"Joueurs participants: {value['players']}",
                                        f"id des tours déjà joués: {value['rounds']}",
                                        f"Règles des partie: {value['game_rules']}",
                                        f"Date de début: {value['begin_date']}",
                                        f"Date de fin: {value['ending_date']}"]
                )
        if choice == 3:
            if sorting == "a":
                report = sorted(Tournament.get_players(tournament_choice), key=lambda x: x.firstname.value.lower())
            if sorting == "c":
                report = sorted(Tournament.get_players(tournament_choice) , key=lambda x: x.elo.value, reverse=True)
            for value in report:
                returned_report.append([f"Prénom: {value.firstname.value}",
                                        f"Nom: {value.lastname.value}",
                                        f"Date de naissance: {value.birth_date.value}",
                                        f"Classement elo: {value.elo.value}",
                                        f"Score dans le tournoi: {value.tournament_score}"])
        if choice == 4:
            report = Tournament.get_tournament_rounds(tournament_choice)
            display = deepcopy(report)
            for value in display:
                try:
                    del value["round_id"]
                    del value["tournament_id"]
                except KeyError:
                    pass
                returned_report.append([f"Nom du tour: {value['name']}",
                                        f"Date de début: {value['beginning_date']}",
                                        f"Date de fin: {value['ending_date']}",
                                        f"Parties jouées: {value['games']}"])
            return returned_report
        if choice == 5:
            first_report = Tournament.get_tournament_rounds(tournament_choice)
            for value in first_report:
                if value["name"] == f"Round {round_choice}":
                    returned_report = value
        return returned_report
