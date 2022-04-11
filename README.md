# Yoshida v0.2.0-alpha

Yoshida is "Card Maker Software" for dynamically creating cards for anything. Design your own Layout and fill the Programm with the needed information. And BOOOM your card is printed.

---

## Usable Parameters for x/y/height/width

For example usage look in "data/card_designs/gamecard_simple.json".

- int
    - the basic format to tell the dimensions in pixel
- percentage
    - "95%"
    - use a string to define percentage which will be calculated from the given height and width
- reverse
    - "!50"
    - use an "!" to subtract from the height or width.
    - if your object is positionied at [x: 0] and [y: 0] while your image has a width of 400, the formula "!50" will make the object 400 - 50 = 350 pixel wide

---
