import eel
from deck_manager import DeckManager

eel.init("web")

dm = DeckManager("config.yaml")

# *** REVIEW ***
@eel.expose
def review_tidbit(rating: int):
    tid = dm.get_next_tidbit()
    if tid == None:
        return None
    
    dm.review_tidbit(tid, rating)
    return dm.deck[0].to_dict()

# *** ADD ***
@eel.expose
def add_tidbit(data: str, usr_question: str, source: str, title: str):
    """
    Creates a new tidbit in the deck

    ## Parameters
    - data: the information to remember
    - usr_question: question passed from user, if empty, model will generate question
    - source: source of the information
    - tite: title of the tidbit
    """

    tid = dm.add_tidbit(data = data, 
                        usr_question = usr_question if usr_question != "" else None,
                        source = source if source != "" else None,
                        title = title if title != "" else None)
    
    # get what ever card is next in the queue
    return dm.deck[0].to_dict()

@eel.expose
def get_deck():
    """
    Returns a list of all the cards in the deck formatted as dictionaries.
    
    ## Returns
    - list of all contents of the deck in dictionary format
    """
    return [tid.to_dict() for tid in dm.deck]

@eel.expose
def get_deck_size():
    """
    Gets the number of entries in the deck
    
    ## Returns
    The number of cards in the deck as an integer
    """
    return len(dm.deck)

# *** SETTINGS ***
@eel.expose
def save_deck():
    """
    Save the deck to the location specified in config.yaml
    """
    dm.save_deck()

@eel.expose
def load_deck():
    """
    Load the deck from the location specified in config.yaml
    """
    return dm.load_deck()



eel.start("index.html")