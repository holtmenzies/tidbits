from fsrs import Card
from datetime import datetime, timezone
class Tidbit():
    """
    A tidbit represents a single piece of information you want to remember.
    Shorter tidbits will more easily produce questions focused on the specified
    content.

    ## Attributes
    - card: Spaced repetion card used to track recall performance
    - data: information to recall
    - title: (optional) title of card
    - tags: (optional) tags used for searching cards by content
    - 
    """    

    def __init__(self,
                 card: Card,
                 data : str,
                 title : str = None,
                 tags : list[str] = None,
                 question : str = None,
                 source : str = None,
                 created: datetime = None
                 ):

        if type(data) is not str or data == "":
            raise ValueError("Data must be a string and cannot be empty")
        self.card = card
        self.data = data
        self.title = title
        self.tags = tags
        self.question = question
        self.source = source
        if created == None or type(created) is not datetime:
            self.created = datetime.now(timezone.utc)
        else:
            self.created = created
        

    def __lt__(self, other: Card):
        """
        Defines the order of two tidbits. This one should comebefore another if
        it has a sooner due date
        
        ## Returns
        True if this card is due for review sooner than another, false otherwise"""
        return self.card.due < other.card.due
    
    def to_dict(self):
        """
        Return tidbit as dict. The card attribute is converted to a dictionary
        as well
        
        ## Returns
        A dictionary representation of the card attributes
        """
        rtn = self.__dict__.copy()
        rtn['card'] = self.card.to_dict()
        rtn['created'] = self.created.isoformat()

        return rtn

    def __str__(self):
        return f"[title: {self.title}, data: {self.data}, question: {self.question}, due: {self.card.due}]"
        
    
