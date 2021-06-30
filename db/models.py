"""
This module is the one communicating with the database.
It is called by the controllers and performs either creation/updates 
or return information from the database

The database used here is TinyDB
"""
import itertools
import json

from datetime import datetime
from tinydb import TinyDB, where, Query
from tinydb.operations import increment, add
from copy import deepcopy

class Field:

    def __init__(self, key, value):
        self.key = key
        self.value = value


class Item:
    """ Turns dictionnary keys into attributs
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # transforme un dictionnaire en objets d'une classe
            setattr(self, key, Field(key, value))

    def __repr__(self):
        return self.to_json()

    def to_json(self):
        item = {}
        for attr in dir(self):
            if isinstance(getattr(self, attr), Field):
                item[attr] = getattr(self, attr).value
        return json.dumps(item)


class Collection:
    """Take a dictionnary in argument and turns items into attributes and corresponding values"""
    def __init__(self, data=None):
        self._items = []
        for item in data:
            self._items.append(Item(**item))

    @property
    def items(self):
        return self._items


class TournamentCollection(Collection):
    """Does the same that Collection but for tournaments"""
    def __init__(self, data=None):
        self._items = []
        for item in data:
            self._items.append(Item(**item))

    @property
    def items(self):
        return self._items


class RoundCollection(Collection):
    """Does the same that Colelction but for Rounds"""
    def __init__(self, data=None):
        self._items = []
        for item in data:

            self._items.append(Item(**item))

    @property
    def items(self):
        return self._items


db = TinyDB('db.json')


class Model:
    """Used as a parent class for orther classes that need to write into the database"""
    def __init__(cls):
        pass

    @classmethod
    def create(cls, attrs):
        cls.__table__.insert(attrs)


class Tournament(Model):
    """Contains all methods used in database relations"""
    __table__ = db.table('tournaments')

    def __init__(self):
        super().__init__()

    @classmethod
    def set_tournament_id(cls):
        """Automatically returns the id of a new tournament 
        It measures the lengh of the table 'tournaments' in the database
        """
        return len(cls.__table__) + 1
    
    @classmethod
    def set_player_id(cls):
        """Automatically returns the id of a new tournament 
        It measures the lengh of the table 'tournaments' in the database
        """
        return len(db.table('players')) + 1
        

    @classmethod
    def get_players(cls, tournament_id):
        """Store players competing in the wished tournament
        It first get the dictionnary of the tournament in the table 'tournaments'
        Secondly it creates a list composed of Player's objects
        Then it sorts this list according to the tournament_score of each player.
        In case of equality it takes the elo rank.
        """
        P = Query()
        tournament = cls.__table__.search(where('id') == tournament_id)

        # on crée notre liste  d'objets players participant au tournoi
        collection = Collection(data=Player.__table__.search(P.id.one_of(tournament[0]["players"])))
        players = sorted(collection.items,
                         key=lambda x: (Tournament.get_tournament_score(
                             x.id.value, tournament_id), x.elo.value),
                         reverse=True)  # on trie cette liste avec l'elo comme critère de trie.

        for player in players:
            setattr(player, 'tournament_score', Tournament.get_tournament_score(
                player.id.value, tournament_id) or 0)
        return players  # on renvoie la liste triée par l'elo des joueurs participants au tournoi.

    @classmethod
    def listing_all_possible_games(cls, tournament_id):
        """Make a list with all possible game configurations
        This is made with a list of all tournament players ids
        and the method combinations from itertools.
        Then cases as [[P1 vs P2], [P2 vs P1]] are avoided
        """
        players = [player.id.value for player in Tournament.get_players(tournament_id)]
        setattr(Tournament, 'list_of_possible_games', [
                game for game in itertools.combinations(players, 2)])
        return Tournament.list_of_possible_games

    @classmethod
    def generate_round(cls, tournament_id):
        """Generate a round according to the tournament ranking and the if it is the first round or not
        Two cases are presents here:
            - if it is the first round of the tournament, one take the sorted list of players
              and split it into two lists. From these two lists each players at the same index of each list
              are confronted.
            - if it is not the first round, one take the sorted list of players. 
              The first of the list encounters the second, the third encounters the fourth and so on
              If the generated game has already occured. For exemple the first vs the second.
              The second of the list shall be replaced by the third and so on until a configuration is found that 
              haven't already been played."""
        nb_of_played_round = db.table('tournaments').get(
            where('id') == tournament_id)['nb_of_played_round']
        nb_rounds = db.table('tournaments').get(
            where('id') == tournament_id)['nb_rounds']
        if nb_of_played_round == nb_rounds:
            return None

        count_rounds = db.table('tournaments').get(
            where('id') == tournament_id)['nb_of_played_round']
        round_id = len(db.table('rounds')) + 1

        is_first_round = count_rounds == 0
        match = []
        players = Tournament.get_players(tournament_id)
        if is_first_round:
            all_possible_games = Tournament.listing_all_possible_games(tournament_id)
            cls.__table__.update({"list_of_possible_games": all_possible_games},
                                 where("id") == tournament_id)
            top = 0
            bottom = int(len(players)/2)
            while top < len(players)/2:
                player_one_id = players[top].id.value
                player_two_id = players[bottom].id.value
                score_one = 0
                score_two = 0
                game = Match(player_one_id, player_two_id, score_one, score_two, count_rounds)
                match.append(game.to_json())

                Match.create({'joueur1': players[top].id.value,
                            'joueur2': players[bottom].id.value,
                            'score_one': 0,
                            'score_two': 0,
                            'round_id': round_id,
                            'match_id': len(db.table('matchs')) + 1})
                top += 1
                bottom += 1
        else:
            copy_players = deepcopy(players)
            ids = []
            while True:
                nb_of_games = 0
                nb_of_players = len(players)
                try:
                    while nb_of_games < nb_of_players/2:
                        authorized_game = False
                        player_one = 0
                        player_two = 1
                        while not authorized_game:
                            player_one_id = copy_players[player_one].id.value
                            player_two_id = copy_players[player_two].id.value
                            score_one = 0
                            score_two = 0
                            if [player_one_id, player_two_id] in db.table('tournaments').search(
                                where("id") == tournament_id)[0]["list_of_possible_games"]:
                                authorized_game = True
                                ids.append([player_one_id, player_two_id])
                                copy_players.remove(copy_players[player_two])
                                copy_players.remove(copy_players[player_one])

                            elif [player_two_id, player_one_id] in db.table('tournaments').search(
                                where("id") == tournament_id)[0]["list_of_possible_games"]:
                                authorized_game = True
                                ids.append([player_two_id, player_one_id])
                                copy_players.remove(copy_players[player_two])
                                copy_players.remove(copy_players[player_one])
                            if authorized_game:
                                game = Match(player_one_id, player_two_id, score_one, score_two, count_rounds)
                                match.append(game.to_json())
                                nb_of_games += 1
                                player_two = 1
                                if len(match) == 4:
                                    for game in ids:
                                        Match.create({'joueur1': game[0],
                                        'joueur2': game[1],
                                        'score_one': 0,
                                        'score_two': 0,
                                        'round_id': round_id,
                                        'match_id': len(db.table('matchs')) + 1})

                                        id_players = game
                                        db.table('tournaments').search(
                                            where("id") == tournament_id)[0]["list_of_possible_games"].remove(id_players)
                                    break
                            else:
                                player_two += 1
                except IndexError:
                    copy_players = deepcopy(players)
                    copy_players[-1], copy_players[-2] = copy_players[-2], copy_players[-1]
                    match = []
                    ids = []

                if len(match) == 4:
                    break
                else:
                    continue

        Round.create({
            'round_id': round_id,
            'tournament_id': tournament_id,
            'name': f"Round {count_rounds + 1}",
            'beginning_date': str(datetime.now()),
            "ending_date": ""
        })
        db.table('tournaments').update(increment('nb_of_played_round'),
                                       where("id") == int(tournament_id))
        db.table('rounds').update({"games": match},
                                  (where("tournament_id") == tournament_id)
                                  & (where("round_id") == round_id))
        round = db.table('rounds').get((where("tournament_id") == tournament_id)
                                       & (where("round_id") == round_id))
        rounds = cls.__table__.get(where("id") == tournament_id)["rounds"]
        rounds.append(round_id)
        db.table('tournaments').update({'rounds': rounds},
                                       where("id") == tournament_id)
        return round

    @classmethod
    def get_game_list(cls, tournament_id_user_choice):
        """Returns the list of games for the ongoing round in the wished tournament"""
        T = Query()
        chosen_tournament = Collection(cls.__table__.search(
            where('id') == tournament_id_user_choice))

        
        

        rounds = RoundCollection(db.table('rounds').search(
            where("tournament_id") == tournament_id_user_choice))

        round_id = rounds.items[chosen_tournament.items[0].nb_of_played_round.value - 1].round_id.value
        if len(rounds.items) == 0:
            return [], None

        games_list = RoundCollection(db.table('matchs').search(
            T.round_id == rounds.items[len(rounds.items) - 1].round_id.value))
        return games_list, round_id

    @classmethod
    def enter_results(cls,
                      tournament_id,
                      round_id,
                      match_id,
                      player_one_score,
                      player_two_score,
                      matchs_results):
        """Updates the results of a round in the database 
        The update is perfomed either in the table rounds and the table matchs
        The method is thought so the user can re-enter results for a game if previous ones were incorrect.
        The method also check if scores are possible as the sum of each player score is expected to be 1
        """
        player_one_id = db.table('matchs').search(where("match_id") == int(match_id))[0]["joueur1"]
        player_two_id = db.table('matchs').search(where("match_id") == int(match_id))[0]["joueur2"]

        db.table('matchs').update({'score_one': player_one_score},
                                  (where('match_id') == match_id) & (where('round_id') == round_id))
        db.table('matchs').update({'score_two': player_two_score},
                                  (where('match_id') == match_id) & (where('round_id') == round_id))

        if [player_one_id, player_two_id] in db.table('tournaments').search(
                where("id") == tournament_id)[0]["list_of_possible_games"]:
            to_remove = [player_one_id, player_two_id]
            db.table('tournaments').search(
                where("id") == tournament_id)[0]["list_of_possible_games"].remove(to_remove)
            list_of_possible_games = db.table('tournaments').search(
                where("id") == tournament_id)[0]["list_of_possible_games"]
            db.table('tournaments').update({"list_of_possible_games": list_of_possible_games},
                                           where("id") == tournament_id)

        game = Match(player_one_id, player_two_id, player_one_score, player_two_score, match_id)

        if db.table('scores').get((where('tournament_id') == tournament_id) & (where("player_id") == player_one_id)):
            db.table('scores').update(add("score", player_one_score), (where('player_id') == player_one_id) & 
                                                                       (where('tournament_id') == tournament_id))
            db.table('scores').update(add("score", player_two_score), (where('player_id') == player_two_id) & 
                                                                       (where('tournament_id') == tournament_id))
        else:
            Score.create({
                "player_id": player_one_id,
                "tournament_id": tournament_id,
                "score": player_one_score
            })
            Score.create({
                "player_id": player_two_id,
                "tournament_id": tournament_id,
                "score": player_two_score
            })

        already_in = False
        for n, match in enumerate(matchs_results):
            if f"[{player_one_id}" in match:
                matchs_results.pop(n)
                already_in = True
                matchs_results.insert(n, game.to_json())

        if not already_in:
            matchs_results.append(game.to_json())

    @classmethod
    def save_results(cls, matchs_results, round_id, tournament_id_user_choice):
        """Updates a round results in the table 'rounds'
        It also give an ending date to the corresponding round"""
        db.table('rounds').update({"games": matchs_results},
                                  (where("tournament_id") == tournament_id_user_choice) &
                                  (where("round_id") == round_id))
        nb_of_played_round = db.table('tournaments').get(
            where('id') == tournament_id_user_choice)['nb_of_played_round']
        nb_rounds = db.table('tournaments').get(
            where('id') == tournament_id_user_choice)['nb_rounds']
        if nb_of_played_round == int(nb_rounds):
            db.table('tournaments').update({"ending_date": str(datetime.now())})

        db.table('rounds').update({"ending_date": str(datetime.now())},
                                    (where("tournament_id") == tournament_id_user_choice) & 
                                    (where("round_id") == round_id))

    @classmethod
    def get_tournament_score(cls, player_id, tournament_id):
        """Calculates the tournament score of a player in a wished tournament
        The method identify all games the player has played in the tournament
        and sums all player's score for each."""
        if not db.table('scores').search(where('tournament_id') == tournament_id):
            return 0

        tournament_score = db.table('scores').get((where('player_id') == player_id) & 
                                                    (where('tournament_id') == tournament_id))
        if tournament_score == None:
            return 0
        return tournament_score["score"]

    @classmethod
    def change_player_elo(cls, player_choice, new_elo):
        """Changes the elo of a player in the table 'players'"""
        P = Query()
        db.table('players').update({'elo': new_elo}, P.id == player_choice)

    @classmethod
    def get_player_info(cls, player_choice):
        """Return the corresponding dictionnary of the wished player"""
        player = db.table('players').get(where('id') == player_choice)
        player_display = [f"Prénom: {player['firstname']}",
                          f"Nom: {player['lastname']}",
                          f"Date de naissance: {player['birth_date']}",
                          f"Classement elo: {player['elo']}",
                          f"Sex: {player['gender']}"]
        return player_display

    @classmethod
    def get_all_players(cls):
        """"Return a list with all components of the 'players' table"""
        return db.table('players').all()
    
    @classmethod
    def get_all_tournaments(cls):
        """"Return a list with all components of the 'tournaments' table"""
        return db.table('tournaments').all()

    @classmethod
    def get_tournament_rounds(cls, tournament_choice):
        """"
        Return a list with all components of the 'rounds' table with 
        the same tournament_id that the value of the parameter tournament_choice
        """
        return db.table('rounds').search(where('tournament_id') == tournament_choice)
    


class Player(Model):
    __table__ = db.table('players')

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return self.__table__[0]["firstname"]


class Match(Model):
    __table__ = db.table('matchs')

    def __init__(self, player_one_id, player_two_id, score_one=0, score_two=0, round_id=None):
        super().__init__()
        self.player_one_id = player_one_id
        self.player_two_id = player_two_id
        self.round_id = round_id
        self.score_one = score_one
        self.score_two = score_two

    def __repr__(self):
        return f"{([self.player_one_id, self.score_one], [self.player_two_id, self.score_two])}"

    def to_json(self):
        return json.dumps(([self.player_one_id, self.score_one],
                           [self.player_two_id, self.score_two]))


class Round(Model):
    __table__ = db.table('rounds')

    def __init__(self, list_of_match, tournament_id=None):
        super().__init__()
        self.tournament_id = tournament_id
        self.list_of_match = list_of_match
        self.begin_date = str(datetime.now())

    def __repr__(self):
        return f"{self.list_of_match}"


class Score(Model):
    __table__ = db.table('scores')

    def __init__(self, player_id, tournament_id, score=None):
        super().__init__()
        self.tournament_id = tournament_id
        self.player_id = player_id
        self.score = score
        