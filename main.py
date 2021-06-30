from views.views import Views


if __name__ == "__main__":
    while True:
        user_choice = Views.main_menue_view()
        try:
            if int(user_choice) == 1:
                Views.create_tournament_view()
                continue
            if int(user_choice) == 2:
                Views.generate_round_view()
                continue
            if int(user_choice) == 3:
                Views.get_round_results_view()
                continue
            if int(user_choice) == 4:
                Views.get_report_view()
                continue
            if int(user_choice) == 5:
                Views.create_player_view()
                continue
            if int(user_choice) == 6:
                Views.get_player_info_view()
                continue
            if int(user_choice) == 7:
                Views.set_new_elo_view()
                continue
            if int(user_choice) == 8:
                Views.show_provisional_ranking()
                continue
            else:
                Views.error_message_view()
                continue
        except ValueError:
            if user_choice in {"q", "Q"}:
                break
            else:
                Views.error_message_view()
                continue