# This script shows an example how to use the Software

import json
import pytest
import os

from modules.Card import Card

cards = []

path = 'data/card_sets/example_game_cards'

def test_card_creation():

    with open(path + '.json', 'r', encoding='utf-8') as example:
        example_json = json.loads(example.read())
        for card in example_json['cards']:
            print('Card:', card)
            cards.append(Card(example_json['design']))
            cards[-1].create(card)
        
        # for card in cards:
        #     card.show()
        # cards[0].show()
        cards[0].card_img.save(path + '_.png')
    
    assert os.path.exists(path + '_.png')

test_card_creation()
