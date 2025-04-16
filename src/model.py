from ollama import Client

class Model():
    """
    Manages the connection the the language model. If a new model API is used it
    should be added here.
    
    ## Attributes
    - connection: name of the languge model to connect to
    """

    def __init__(self, connection : str, **kwargs):
        """
        Initializes the connection the the model
        
        ## Parameters
        - connection: name of the model to connect to
        - kwargs: params that are specific to the language model connection,
        should include anything needed to establish the connection
        """
        self.model_client = None
        self.connection = connection
        if connection == 'ollama':
            self.model_client = OllamaClient(**kwargs)
        else:
            raise ValueError(f"Invalid Model Connection: {connection}")
        
        # TODO IO block, could be good to async
        try:
            self.model_client.client.list()
        except ConnectionError:
            self.model_client = None
        
    def get_question_prompt(self):
        """
        Returns the current prompt for generating questions
        
        ## Returns
        Current prompt for generating questions as a string
        """
        return self.model_client.question_prompt

    def generate_question(self, data):
        return self.model_client.generate_question(data)['message']['content']
    
    def get_answer_prompt(self):
        """
        Returns the current prompt used to evaluate answers
        
        ## Returns
        Current prompt used to evaluate answers as a string"""
        return self.model_client.answer_prompt
    
class ModelClient():
    """
    Interface for Model client connections. This interface is agnostic to the
    language model interface.
    
    All implementations of a model client should implement the functions in this
    class
    """
    
    def __init__(self, 
                 question : str = None,
                 answer : str = None):
        """
        Parent constructor for model clients. Setup params are delegated to the
        child classes for each type of client. If no system message for
        'question' or 'answer' ar provided defaults are passed
        
        ## Parameters
        - question: system prompt used to generate flashcard questions
        - answer: system prompt used to evaluate answers
        """
        self.question_prompt = question
        self.answer_prompt = answer
        if question == None:
            self.question_prompt = """Create a question based on the following information:"""
        if answer == None:
            self.answer_prompt = """Evalute the following input on a scale from 1 to 5. With 5 being the best"""

    def generate_question(self):
        raise NotImplementedError()

    def eval_answer(self):
        raise NotImplementedError()
    
    def generate_tags(self):
        raise NotImplementedError()
    
    def generate_title(self):
        raise NotImplementedError()
    
    def close_connection(self):
        raise NotImplementedError()
    
    
class OllamaClient(ModelClient):
    """Connection to an ollama model"""

    def __init__(self,
                 model_type : str,
                 host : str = 'http://localhost:11434',
                 headers : dict = None,
                 question : str = None,
                 answer : str = None):
        """
        Creates an instance of a connection to an ollama client
        ## Parameters
        - model_type: type supported by ollama
        - host: address of ollama server, likely localhost:11434
        - headers: optional, parameters used for server connection
        - question: prompt used to generate quiz questions
        - answer: prompt used to evaluate answers
        """
        
        super().__init__(question, answer)
        self.model_type = model_type
        self.client = Client(
            host = host,
            # headers = headers
        )
     
    def generate_question(self, data : str):
        """
        Generates a question about the data passed using the current prompt and
        returns the result as a string

        ## Paramerters
        - data: information used to generate a question

        ## Returns
        A new question about the data
        """
        return self.client.chat(model = self.model_type,
                         messages = [{
                             'role' : 'system',
                             'content' : self.question_prompt
                         },
                         {
                             'role' : 'user',
                             'content' : data
                         }])        
    
    def close_connection(self):
        """
        Ollama does not require the connection to the server to close.
        """
        return True

