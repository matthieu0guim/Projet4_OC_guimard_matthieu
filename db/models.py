import itertools, json

from datetime import datetime
from tinydb import TinyDB, where, Query
from tinydb.operations import increment 

class Field:

    def __init__(self, key, value):
        self.key = key
        self.value = value


class Item:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, Field(key, value)) # transforme un dictionnaire en objets d'une classe
        
    def __repr__(self):
        return self.to_json()
   
    def to_json(self):
        item = {}
        for attr in dir(self):
            if isinstance(getattr(self, attr), Field):
                item[attr] = getattr(self, attr).value 
        return json.dumps(item)


class Collection:
    
    # _items = [] # probleme avec cet attribut de classe: quand on utilise plusieurs fois la classe les resultats s'accumulent dans cette liste.
    
    def __init__(self, data=None):
        self._items = []
        for item in data:
            self._items.append(Item(**item))
    

    @property
    def items(self):
        return self._items

class TournamentCollection(Collection):
    # _items = []
    def __init__(self, data=None):
        self._items = []
        for item in data:
            
            self._items.append(Item(**item))

    @property
    def items(self):
        return self._items
    
class RoundCollection(Collection):
    # _items = []
    def __init__(self, data=None):
        self._items = []
        for item in data:
            
            self._items.append(Item(**item))

    @property
    def items(self):
        return self._items

db = TinyDB('db.json')


class Model:
    def __init__(cls):
        pass

    @classmethod
    def create(cls, attrs):
        cls.__table__.insert(attrs)


class Tournament(Model):
    __table__ = db.table('tournaments')
    
    def __init__(self):
        super().__init__()
    
    @classmethod
    def set_players(cls, tournament_id, player_ids):
        cls.__table__.update({'players': player_ids}, where('id') == tournament_id)
        
    @classmethod
    def get_players(cls, tournament_id):
        P = Query()
        tournament = cls.__table__.search(where('id') == tournament_id)

        collection = Collection(data=Player.__table__.search(P.id.one_of(tournament[0]["players"]))) # on crée notre liste  d'objets players participant au tournoi
        
        players = sorted(collection.items, key=lambda x: (Tournament.get_tournament_score(x.id.value,tournament_id), x.elo.value),
                                                                                          reverse=True) # on trie cette liste avec l'elo comme critère de trie.
        for player in players:
            setattr(player, 'tournament_score', Tournament.get_tournament_score(player.id.value,tournament_id))
        return players # on renvoie la liste triée par l'elo des joueurs participants au tournoi.

    @classmethod
    def listing_all_possible_games(cls, tournament_id):
        
        players = [ player.id.value for player in  Tournament.get_players(tournament_id)]
        setattr(Tournament, 'list_of_possible_games', [game for game in itertools.combinations(players, 2)])
        return Tournament.list_of_possible_games

    @classmethod
    def generate_round(cls, tournament_id_user_choice):
        if db.table('tournaments').search(where('id') == tournament_id_user_choice)[0]['nb_of_played_round'] == db.table('tournaments').search(where('id') == tournament_id_user_choice)[0]['nb_rounds']:
            print("Votre tournoi est terminé. Il n'est plus possible de jouer de tours supplémentaires.")
            return None
        
        count_rounds = db.table('tournaments').search(where('id') == tournament_id_user_choice)[0]['nb_of_played_round']
        round_id = len(db.table('rounds')) + 1
               
        is_first_round = count_rounds == 0
        if is_first_round:
            all_possible_games = Tournament.listing_all_possible_games(tournament_id_user_choice)
            cls.__table__.update({"list_of_possible_games": all_possible_games}, where("id") == tournament_id_user_choice)
        Round.create({
            'round_id': round_id,
            'tournament_id': tournament_id_user_choice,
            'beginning_date': str(datetime.now())
        })
 
        players = Tournament.get_players(tournament_id_user_choice)
        match = []
        
        top = 0
        bottom = int(len(players)/2)
        while top < 4:
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
                          'match_id': top})
            top += 1
            bottom += 1
        
        db.table('rounds').update({"games": match}, (where("tournament_id") == tournament_id_user_choice)
                                                    & (where("round_id") == round_id))
        round = db.table('rounds').search((where("tournament_id") == tournament_id_user_choice)
                                                    & (where("round_id") == round_id))
        db.table('tournaments').update({'rounds': round_id}, where("id") == tournament_id_user_choice)
        return round

    @classmethod
    def get_tournament_list(cls):
        tournament_list = Collection(cls.__table__.search(where('id') != 0))
        return tournament_list

    @classmethod
    def get_game_list(cls, tournament_id_user_choice):
        T = Query()
        chosen_tournament = Collection(cls.__table__.search(where('id') == tournament_id_user_choice))
        db.table('tournaments').update(increment('nb_of_played_round'), where("id") == int(tournament_id_user_choice))
        round_id = chosen_tournament.items[0].nb_of_played_round.value
        
      
        rounds = TournamentCollection(db.table('rounds').search(where("tournament_id") == tournament_id_user_choice 
                                                                and where("round_id") == round_id))
        print('la')
        print(rounds.items)
        if len(rounds.items) == 0:
            return None, "rounds.items est vide", tournament_id_user_choice, round_id
        print('re')
        games_list = RoundCollection(db.table('matchs').search(T.round_id == rounds.items[0].round_id.value))
        print('ici', games_list, round_id)
        return games_list, round_id

    @classmethod
    def enter_results(cls, tournament_id_user_choice, round_id, match_id, player_one_score, player_two_score, matchs_results):
        player_one_id = db.table('matchs').search(where("match_id") == int(match_id))[0]["joueur1"]
        player_two_id = db.table('matchs').search(where("match_id") == int(match_id))[0]["joueur2"]
        
        db.table('matchs').update({'score_one': player_one_score}, (where('match_id') == match_id) & (where('round_id') == round_id))
        db.table('matchs').update({'score_two': player_two_score}, (where('match_id') == match_id) & (where('round_id') == round_id))
        
        if [player_one_id,player_two_id] in db.table('tournaments').search(where("id") == tournament_id_user_choice)[0]["list_of_possible_games"]:
            db.table('tournaments').search(where("id") == tournament_id_user_choice)[0]["list_of_possible_games"].remove([player_one_id, player_two_id])
            list_of_possible_games = db.table('tournaments').search(where("id") == tournament_id_user_choice)[0]["list_of_possible_games"]
            db.table('tournaments').update({"list_of_possible_games": list_of_possible_games}, where("id") == tournament_id_user_choice)
        
        game = Match(player_one_id, player_two_id, player_one_score, player_two_score, match_id)
        
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
        db.table('rounds').update({"games": matchs_results}, (where("tournament_id") == tournament_id_user_choice) &
                                                            (where("round_id") == round_id))
    
    
    @classmethod
    def get_tournament_score(cls, player_id, tournament_id):
        
        tournament_score = 0
        if db.table('matchs').search((where('joueur1') == player_id) | (where('joueur2') == player_id)) == []:
            return 0
        
        for d in db.table('matchs').search((where('joueur1') == player_id) | (where('joueur2') == player_id)):
            
            id_liste = [k for k, v in d.items() if v == player_id and 'joueur' in k]
            score_liste = [d['score_one'] if id_liste[-1] == 'joueur1' else d['score_two']]
            tournament_score += score_liste[-1]
        
        return tournament_score

    @classmethod
    def change_player_elo(cls):
        while True:
            P = Query()
            liste_of_players = db.table('players')
            print(liste_of_players.all())
            player_id = input("Id du joueur à modifier: ")
            if player_id == 'Q' or player_id == 'q':
                break
            new_elo = input("nouveau classement elo du joueur:")
            if new_elo == 'Q' or new_elo == 'q':
                break
            if len(db.table('players').search(where('id') == int(player_id))) == 0:
                print("votre joueur n'existe pas dans notre base de données...")
            db.table('players').update({'elo': int(new_elo)}, P.id == int(player_id))

        # afficher la liste des joueurs, on choisit le joueur, spécifier le nouveau elo, tant qua pas appuyé sur Q: FINIE
        # TODO : tout ce qui est affichage à l'écran devra être déplacé dans VIEWS
    


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
        return json.dumps(([self.player_one_id, self.score_one], [self.player_two_id, self.score_two]))
    


class Round(Model):
    __table__ = db.table('rounds')
    def __init__(self, list_of_match, tournament_id=None):
        super().__init__()
        self.tournament_id = tournament_id
        self.list_of_match = list_of_match
        self.begin_date = str(datetime.now())
    def __repr__(self):
        return f"{self.list_of_match}"