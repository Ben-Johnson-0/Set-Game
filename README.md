# Set Game

A recreation of the card game Set by Marsha Falco.
[Set Wiki Page](https://en.wikipedia.org/wiki/Set_(card_game))

## Installation

Clone the repository:

```bash
git clone https://github.com/Ben-Johnson-0/Set-Game.git
cd set-game
```
Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the game
```bash
python gui.py
```

## Goal

The goal is for player(s) to find sets of three cards. A set is a group of cards where each of the attributes of the cards are either all the same variation or none of them are the same.


## Cards

Cards have 4 different attributes with each attribute having 3 variations.
| Shape   | Color  | Number | Shading |
| ------- | ------ | ------ | ------- |
| Oval    | Red    | 1      | Solid   |
| Tilde   | Green  | 2      | Striped |
| Diamond | Purple | 3      | Open    |


## Gameplay Overview

1. Twelve cards are dealt face-up.

2. Players look for valid sets of three cards.

3. When a set is found, those cards are replaced with new ones from the deck.

4. The game continues until the deck is exhausted and no sets remain or the board no longer contains any sets.


## Features

* Randomized deck generation (81 unique cards)

* Set validation logic that follows official game rules

* Auto-detecting function

## Planned Features

* Prettier GUI

* Hint highlighting

* Sound Effects

## License

This project is an open-source, educational recreation of Set and is not affiliated with Set Enterprises, Inc.
