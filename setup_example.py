# This script shows an example how to use the Software

import json

from modules.Card import Card

cards = []

with open('data/card_sets/example_cards.json', 'r', encoding='utf-8') as example:
    example_json = json.loads(example.read())
    for card in example_json['cards']:
        print(card)
        cards.append(Card(example_json['design']))
        cards[-1].create(card)
    
    # for card in cards:
    #     card.show()
    cards[0].show()
