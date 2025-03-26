import pytest
from model import Model


def test_model():

    with pytest.raises(ValueError):
        Model(connection = 'NotSupportedModel',
            model_type = 'llama3.2:1b',
            host = 'http://localhost:11434')
        
    # Check default question
    m = Model(connection = 'ollama',
            model_type = 'llama3.2:1b',
            host = 'http://localhost:11434')
    assert m.get_question_prompt() == "Create a question based on the following information:"
    assert m.get_answer_prompt() == "Evalute the following input on a scale from 1 to 5. With 5 being the best"
    
    # check custom question
    m = Model(connection = 'ollama',
            model_type = 'llama3.2:1b',
            host = 'http://localhost:11434',
            question = "Create question a on the following information. Do not include reasoning for why the question is asked."
            )
    assert m.get_question_prompt

def test_connection():
    m = Model(connection = 'ollama',
            model_type = 'llama3.2:1b',
            host = 'Not a Host')
    
    assert m.model_client == None
    
   