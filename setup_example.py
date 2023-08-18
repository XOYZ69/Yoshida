# This script shows an example how to use the Software

import json
import pytest
import os
import shutil

from modules.Card import Card

def test_card_creation_basis(card_set = '', show = False):

    print('Testing card set:', card_set)

    save_location = 'data/output/{card_set}/'.format(card_set = card_set)

    # Cleanup old files from testing
    if os.path.exists(save_location):
        shutil.rmtree(save_location)

    os.makedirs(save_location, exist_ok = True)

    cards = []

    json_file = 'data/card_sets/{card_set}.json'.format(card_set = card_set)

    if card_set == '':
        print('Empty card set is detected correctly.')
        assert True
        return

    assert os.path.exists(json_file), 'The json file does not exist. Please make sure to enter the correct card_set'

    with open(json_file, 'r', encoding = 'utf-8') as example:
        example_json = json.loads(example.read())

        card_count = 0

        for card in example_json['cards']:
            
            cards.append(Card(example_json['design']))

            cards[-1].create(card)

            card_count += 1

            if 'var_id' in card:
                filename = card['var_id'] + '.png'
            else:
                filename = str(card_count) + '.png'
            
            cards[-1].card_img.save(save_location + filename)

            print('Card {card} completed.'.format(card = filename))

            if show:
                cards[-1].card_img.show()
            
            assert os.path.exists(save_location + filename), 'Generated file does not exist.'

def test_gamecard_simple():
    test_card_creation_basis('example_gamecard_simple')

def test_yugioh():
   test_card_creation_basis('example_yu-gi-oh')

def test_cocktail():
    test_card_creation_basis('example_cocktails')
