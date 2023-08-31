# Yoshida

**⚠️ This description is due to time restraints not up to date! ⚠️**

**Sorry for the inconvenience**

Yoshida is "Card Maker Software" for dynamically creating cards for anything. Design your own Layout and fill the Programm with the needed information. And BOOOM your card is printed.

---

### Stability information

The newest release of Yoshida always supports everything used in the example [designs](https://github.com/XOYZ69/Yoshida/tree/master/data/card_designs) and [sets](https://github.com/XOYZ69/Yoshida/tree/master/data/card_sets) since they are getting tested with every commit.
If anything does not work please check if there are any new versions out or create a [new issue](https://github.com/XOYZ69/Yoshida/issues/new/choose).

With that said until Version 1.0 is released this program should be used with these things in mind.

[![Current Yoshida Version](https://img.shields.io/github/v/release/XOYZ69/Yoshida.svg?sort=semver)](https://github.com/XOYZ69/Yoshida/releases/latest)
[![Version 1.0 Release Progress](https://img.shields.io/github/milestones/progress-percent/XOYZ69/Yoshida/1)](https://github.com/XOYZ69/Yoshida/milestone/1)

[![Minimum Python Version](https://img.shields.io/badge/Required_python_version-3.10_+-blue.svg)](https://www.python.org/downloads/release/python-3100/)

[![Unit Test Designs](https://github.com/XOYZ69/Yoshida/actions/workflows/unit_test_designs.yml/badge.svg)](https://github.com/XOYZ69/Yoshida/actions/workflows/unit_test_designs.yml)



## Setup

## Setup

1. Clone the repo or download the newest release from the [release page](https://github.com/XOYZ69/Yoshida/releases).

    ```
    gh repo clone XOYZ69/Yoshida
    ```
    or
    ```
    git clone https://github.com/XOYZ69/Yoshida
    ```
    
    The newest release can be found here:

    [![Current Yoshida Version](https://img.shields.io/github/v/release/XOYZ69/Yoshida.svg?sort=semver)](https://github.com/XOYZ69/Yoshida/releases/latest)

2. Create your own card design (wiki entries will follow) or use an exisiting one in the folder ```data/card_designs```.

    ```
    Yoshida/
        data/
            card_designs/
                designs.json
    ```

3. Add a new card set in `data/card_sets` for your card design or use an existing one.

    ```
    Yoshida/
        data/
            card_sets/
                set.json
    ```

4. Edit the `setup_example.py` to include ` test_card_creation_basis(card_set = your_card_set, show = False)`
    
    `card_set` is the name of your card set
    
    `show` is a boolean defining if you want to open your exported card instantly or only save it in the `data/output` folder.

5. Call your function from the file and run it with `python setup_example.py` or simply call `pytest -rA setup_example.py` to run all tests.

    ```
    test_card_creation_basic(card_set = your_card_set, show = True)
    ```

6. The finished images are created in the folder `data/output/card_set`


---
