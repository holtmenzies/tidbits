from model import Model
from tidbit import Tidbit
from json import load as j_load, dump as j_dump
from fsrs import Scheduler, Card, Rating
import yaml
from heapq import heappush, heappop
from datetime import datetime
from time import sleep


class DeckManager():
    """
    Manages the state of the deck of spaced repetion cards. On construction
    config.yaml is loaded. If the program has been run previously then the
    scheduler and deck of cards last used are loaded by default, otherwise a new
    scheduler and deck are created. The scheduler is only responsible for
    maintaining the parameters of the spaced repetion model. A heap is used to
    pull the next card to be reviewed.
    
    ## Attributes
    - config: configuration for location of deck, model prompts, and params for
    connecting to a model server
    - deck: priority queue of tidbits ordered by time for review
    - schedule: scheduler for reviewing tidbits
    - config_file_path: location of config file
    """

    def __init__(self, config_file_path : str):
        """
        Starts up the deck manager. If a previous configuration has been used,
        that will be loaded. If no deck has been created previously then a new
        scheduler and new set of cards will be created

        ## Parameters
        - config_file_path: location of configuration file
        """
        self.config = None
        with open(config_file_path, 'r') as config:
            self.config = yaml.safe_load(config)
        self.config_file_path = config_file_path
        self.deck = [] # heap used for priority queue
        self.schedule = None

        # TODO IO block -- could be good to async
        if self.config['initialized']:
            self.load_deck(self.config['deck'])
        else:
            self.schedule = Scheduler()

        # Need to handle error when model server is not up
        self.model = Model(
                **self.config['model params'],
                question = self._load_prompt(self.config['question']),
                answer = self._load_prompt(self.config['answer'])
            )
        
    
    def add_tidbit(self, data, title = None, gen_title = False, gen_tags = False, **kwargs):
        """
        Adds a new piece of information to the deck. The deck is treated as 
        'initialized' once at least one card has been added to the deck.
        
        ## Params
        - data: information to recall
        - gen_title: boolean flag, if True model will create a title for the 
        tidbit
        - gen_tags: boolean flag, if True model will generate a set of tags 
        describing the content
        - kwargs: other optional params passed to the tidbit

        ## Returns
        A reference to the new tidbit
        """
        card = Card()
        # title = None
        tags = None
        if gen_title:
            title = self.model.generate_title(data)
        if gen_tags:
            tags = self.model.generate_tags(data)
        question = self.model.generate_question(data)
        tid = Tidbit(card, data, title, tags, question, **kwargs)
        heappush(self.deck, tid)
        self.config['initialized'] = 'true'
        return tid

    def get_next_tidbit(self):
        """
        Removes and returns the next tidbit to review from the deck

        ## Returns
        Tidbit with closest time for review or None if deck is empty
        """
        if len(self.deck) == 0:
            return None
        return heappop(self.deck)
    
    def review_tidbit(self, tidbit : Tidbit,
                      rating : Rating):
        rev_card = tidbit.card
        rev_card, _ = self.schedule.review_card(rev_card, rating)
        tidbit.card = rev_card
        heappush(self.deck, tidbit)
    
    def pause_card(self, tidbit: Tidbit):
        """
        Prevent a card from being reviewed, but not delete it

        ## Params
        - tidbit: card to pause
        """
        raise NotImplementedError()
    
    def delete_card(self, tidbit: Tidbit):
        """
        Remove card entirely from the deck
        """
        raise NotImplementedError
    
    def _load_prompt(self, file_path):
        """
        Load a prompt from a given text file
        
        ## Params
        - file_path: location of prompt to read
        
        ## Raises
        - ValueError: if file_path is not for a text file
        """

        if file_path.split('.')[-1] != 'txt':
            raise ValueError("Prompt must be a text file")
        
        try:
            with open(file_path, 'r') as file:
                prompt = file.read()
                if prompt == "":
                    return None
                return prompt
        except FileNotFoundError:
            return None
        
    def _parse_tidbit(self, tidbit_dict):
        """
        Parses a tidbit from a json formatted string
        
        ## Params
        - tidbit_dict: json formatted string describing tidbit

        ## Returns
        A tidbit with the params passed from a file
        """
        tidbit_dict['card'] = Card.from_dict(tidbit_dict['card'])
        tidbit_dict['created'] = datetime.fromisoformat(tidbit_dict['created'])
        return Tidbit(**tidbit_dict)

    def load_deck(self, file_path = None):
        """
        Builds a deck and scheduler from a json formatted file
        
        ## Params
        -file_path: location of deck file

        ## Returns
        True is deck is successfully loaded False if there are no cards
        
        ## Raises
        - ValueError if file_path is not for a json file
        """
        file_path = self.config['deck'] if file_path == None else file_path

        if file_path.split('.')[-1] != 'json':
            raise ValueError("Deck must be in json format")
        with open(file_path, 'r') as file:
            deck = j_load(file)
            temp_schedule = Scheduler.from_dict(deck['schedule'])
            temp_deck = [self._parse_tidbit(t) for t in deck['deck']]
            if len(temp_deck) <= 0:
                return False
            
            self.schedule = temp_schedule
            self.deck = temp_deck
            return True


    def save_deck(self, file_path = None):
        """
        Write the contents of the deck and the state of the scheduler to a 
        json file. If no location is specifed then the location specifed by the
        config attribute is used. After the first time a deck is saved,
        config.yaml is updated to the initialized state.

        ## Params
        - file_path: location to save the deck to
        
        """
        file_path = self.config['deck'] if file_path == None else file_path

        # contents of deck are stored in their current ordering
        update = {
            'deck' : [t.to_dict() for t in self.deck],
            'schedule' : self.schedule.to_dict()
        }
        
        with open(file_path, 'w', encoding = 'utf-8') as file:
            j_dump(update, file, ensure_ascii = False, indent = 4)
        


    def quit(self, file_path = None):
        """
        NOT YET IMPLEMENTED
        
        Saves the current deck and updates the config file
        """
        raise NotImplementedError()
    
        self.save_deck(file_path)
        with open(self.config_file_path, 'w') as file:
            pass

    def reset(self):
        """
        Resets the state of the deck and scheduler
        """

        self.deck = []
        self.schedule = Scheduler()


if __name__ == '__main__':
    dm = DeckManager("config.yaml")

    dm.add_tidbit("Albert has 23 sheep", source = "some-place.com")
    sleep(2)
    dm.add_tidbit("Bill has 99 goats", source = "another-place.net")
    sleep(2)
    dm.add_tidbit("Casey has 38 opossums")

    dm.save_deck('test.json')


