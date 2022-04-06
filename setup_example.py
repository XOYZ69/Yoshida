# This script shows an example how to use the Software

from modules.Card import Card

c = Card('gamecard_simple')
c.create(
    {
        'setname': 'Game Cards',
        "var_background": "RED"
    }
)
c.show()
