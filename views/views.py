from db.models import Tournament
from controllers.app import AppController


class Views:

    def enter_results_view():
        pass
    
    
    @staticmethod
    def generate_round_view():
        print(f"Pour quel tournoi voulez-vous générer un round? \n ")
        tournament_id = input()
        return tournament_id
    
    @staticmethod
    def show_generated_round(round):
        print(round[0]['games'])

    @staticmethod
    def enter_results_view(tournament_list):
        print(f"Pour quel tournoi voulez-vous rentrer les résultats?")
        for tournament in tournament_list.items:
            print(f"id: {tournament.id.value}, name: {tournament.name.value}")
        tournament_id_user_choice = input()
        return tournament_id_user_choice
        