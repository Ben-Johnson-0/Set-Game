"""
https://en.wikipedia.org/wiki/Set_(card_game)

Card Attributes
 Shapes: 
    diamond, tilde, oval
 Colors:
    red, green, purple
 Numbers of shapes:
    1, 2, 3
 Shading:
    solid, striped, open

Num of Matches by attributes: (Groups)
 0 same, 4 diff = 648
 1 same, 3 diff = 1296
 2 same, 2 diff = 972
 3 same, 1 diff = 324
"""
import numpy as np
from itertools import product

N_ATTRIBUTES = 4
N_VARIANTS = 3

def generate_deck() -> np.array:
    """
    Generate the 81-card Set deck as a NumPy array of shape (81, 4).
    Each row represents one card, with 4 integer attributes (0–2).
    
    Example card representation:
        [shape, color, number, shading]
    
    Returns:
        np.ndarray: Full deck with values in [0, N_VARIANTS-1].
    """
    deck = np.array(list(product(range(N_VARIANTS), repeat=N_ATTRIBUTES)), dtype=np.int8)
    return deck


class SetGame:
    def __init__(self, board_size:int = 12):
        self.deck = generate_deck()
        np.random.shuffle(self.deck)

        self.cards_drawn = board_size
        self.board = self.deck[:self.cards_drawn]
        self.selected = []  # Card indices selected by a player
        self.matches = 0

    
    def is_set(self, potential_set: np.array) -> bool:
        """
        Checks if an np.array of shape (N_VARIANTS, N_ATTRIBUTES) is a set.
        A set is defined as N_VARIANTS cards where each attribute is either all the same or all different.
        """
        if potential_set.shape != (N_VARIANTS, N_ATTRIBUTES):
            print(f"{__name__} defaulting to return False. Expected potential_set to be of shape {(N_VARIANTS, N_ATTRIBUTES)}, but received shape {potential_set.shape}.")
            return False

        # The sum of each attribute (column) must be evenly divisible by the number of variants attributes
        sums = np.sum(potential_set, axis=0)
        mods = np.mod(sums, N_VARIANTS)

        # If all of the mod operations return 0 then it's a set
        return (np.sum(mods) == 0)

    def find_set(self, new_indices: list | None = None) -> tuple:
        """
        Searches the board array for a set.
        starts with the 3 newest added cards to a board

        Args:
        board (np.array): The gameboard of cards in the form of their own smaller np.arrays of their attributes.
        new_indices (list | None): An optional list of indices that have been changed since the last time find_set was run.

        Returns:
        tuple (bool, np.array | None, int): isFound (bool), set indices (np.array | None), number of cards checked (int)
        
        """

        index_search_order = range(self.board.shape[0])

        # Search for matches trying the newest cards first. Defaults to index order for the first search of a board
        if new_indices:
            for x in new_indices:
                index_search_order.remove(x)
            index_search_order = new_indices + index_search_order

        cards_checked = 0
        for iteration, i in enumerate(index_search_order):
            cards_checked += 1
            initial_card = self.board[i]
            # Look for cards with the best options

            # Each group is based off the number of matching attributes, group[0] is all indices with 0 shared attributes and so on
            groups = [[], [], [], []]
            for k in index_search_order[iteration+1:]:
                n_matches = np.sum(np.equal(initial_card, self.board[k]))
                groups[n_matches].append(k)

            # Search relevant groups for sets
            for group in groups:
                # Not enough cards to make a set
                if len(group) < 2:
                    continue

                # Pick a 2nd card, k, in a big enough group and check within the group for a set
                for j, k in enumerate(group):
                    for x in group[j+1:]:
                        cards_checked += 1
                        potential_set = np.array([initial_card, self.board[k], self.board[x]])
                        if self.is_set(potential_set):
                            return True, np.array([i, k, x]), cards_checked

        return False, None, cards_checked

    def replace_cards(self, indices: list):
        """Replace given card indices on the board with new cards"""

        # If there are no cards left in the deck, delete the indices instead of drawing
        cards_left :int = len(self.deck) - self.cards_drawn
        if len(indices) > cards_left - len(indices):
            print("Deleting 3 indices")
            self.board = np.delete(self.board, indices, axis=0)
            return

        # Replace cards that were made into a set
        self.board[indices] = self.deck[self.cards_drawn : self.cards_drawn + len(indices)]
        self.cards_drawn += len(indices)

    def play_self(self):
        """Automatically plays through an entire game of Set and prints statistics"""
        checks = 0
        print("Starting board\n", self.board)

        while self.cards_drawn < len(self.deck):
            isFound, indices, n_checked = self.find_set()
            checks += n_checked
            if not isFound:
                print(f"Failed to find set in {checks} tries. Found {self.matches} matches total.")
                return
            self.matches += 1
            self.replace_cards(indices)
            print("Match:", indices)
        
        print("Final board\n", self.board)
        print(f"Found {self.matches} through {checks} card checks.")

    def select_card(self, idx):
        """Toggles selection of a card on the board"""
        if idx in self.selected:
            self.selected.remove(idx)
        
        elif len(self.selected) < N_VARIANTS:
            self.selected.append(idx)
    
    def submit_selection(self):
        """Checks whether a selection of cards is valid, returns that value and updates the game state"""
        if len(self.selected) != N_VARIANTS:
            return False

        cards = np.array(self.board[self.selected])
        if self.is_set(cards):
            self.matches += 1
            self.replace_cards(self.selected)   # Replace indices rather than values
            self.selected.clear()
            return True
        

if __name__ == "__main__":
    print("Run gui.py for a user-friendly interface.")
    game = SetGame()
    game.play_self()
