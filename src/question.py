from collections import deque

class Question():
    """
    Represents a question or set of questions tied to a given card.
    """

    data : str
    questions: list[str]
    
    def __init__(self,
                 data : str):
        """
        Generates a new question"""
        pass