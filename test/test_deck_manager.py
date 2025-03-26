import pytest
from deck_manager import DeckManager
from fsrs import Scheduler, Card, Rating, ReviewLog

def test_DeckManager():
    """
    Tests the constructor when the model is live
    """
    dm = DeckManager('src/config.yaml')
    assert len(dm.deck) == 0

    dm = DeckManager('test/config_1.yaml')
    assert dm.model.model_client == None

    dm = DeckManager('test/config_2.yaml')
    assert dm.model.get_question_prompt() == "This is a short prompt"

@pytest.mark.skip(reason = "Very slow to run")
def test_tidbit():
    """
    Tests adding a new tidbit to the deck
    """
    dm = DeckManager("src/config.yaml")

    dm.add_tidbit("Albert has 23 sheep", source = "some-place.com")
    c = dm.deck[0]
    assert c.title == None
    assert c.data == "Albert has 23 sheep"
    assert c.source == "some-place.com"

    dm.add_tidbit("Bill has 99 goats", source = "another-place.net")
    c = dm.deck[1]
    assert c.data == "Bill has 99 goats"
    assert c.source == "another-place.net"

    dm.add_tidbit("Casey has 38 opossums")
    assert dm.deck[2].data == "Casey has 38 opossums"

def test_review_tidbit():
    """
    Tests adding reviewed cards back to the deck
    """
    dm = DeckManager("test/config_3.yaml")

    dm.add_tidbit("Albert has 23 sheep", source = "some-place.com")
    dm.add_tidbit("Bill has 99 goats", source = "another-place.net")
    dm.add_tidbit("Casey has 38 opossums")

    dm.review_tidbit(dm.get_next_tidbit(), Rating.Easy)
    dm.review_tidbit(dm.get_next_tidbit(), Rating.Easy)
    dm.review_tidbit(dm.get_next_tidbit(), Rating.Again)
    assert "Albert has 23 sheep" == dm.deck[0].data
    assert "Casey has 38 opossums" == dm.deck[1].data
    assert "Bill has 99 goats" == dm.deck[2].data

def test_load_deck():
    """
    Test loading a deck from a json file
    """
    dm = DeckManager("test/config_3.yaml")
    assert 3 == len(dm.deck)
    assert "Albert has 23 sheep" == dm.deck[0].data
    assert "Bill has 99 goats" == dm.deck[1].data
    assert "Casey has 38 opossums" == dm.deck[2].data

    assert not dm.load_deck("test/empty_deck.json")


if __name__ == '__main__':
    pytest.main()