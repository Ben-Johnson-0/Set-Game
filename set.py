"""
https://en.wikipedia.org/wiki/Set_(card_game)

Card Attributes
 Numbers of shapes:
    1, 2, 3
 Colors:
    red, green, purple
 Shapes: 
    diamond, tilde, oval
 Shading:
    solid, striped, open

Num of Matches by attributes: (Groups)
 0 same, 4 diff = 648
 1 same, 3 diff = 1296
 2 same, 2 diff = 972
 3 same, 1 diff = 324
"""
import numpy as np

N_ATTRIBUTES = 4
N_VARIANTS = 3

def generate_deck() -> np.array:
    """
    Creates the 81 card deck from the game Set as an np.array of shape (81,4).
    """
    deck = []
    options = range(N_VARIANTS)
    for i in options:
        for j in options:
            for k in options:
                for l in options:
                    deck.append([i, j, k, l])
    return np.array(deck, dtype=np.int8)

def check_set(potential_set: np.array) -> bool:
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


class SetGame:
    def __init__(self, board_size:int = 12):
        self.deck = generate_deck()
        np.random.shuffle(self.deck)

        self.cards_drawn = board_size
        self.board = self.deck[:self.cards_drawn]

    
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
                        if check_set(potential_set):
                            return True, np.array([i, k, x]), cards_checked

        return False, None, cards_checked

    def replace_cards(self, indices: list):
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
        matches =  0
        checks = 0
        print("Starting board\n", self.board)

        while self.cards_drawn < len(self.deck):
            isFound, indices, n_checked = self.find_set()
            checks += n_checked
            if not isFound:
                print(f"Failed to find set in {checks} tries. Found {matches} matches total.")
                return
            matches += 1
            self.replace_cards(indices)
            print("Match:", indices)
        
        print("Final board\n", self.board)
        print(f"Found {matches} through {checks} card checks.")
        

if __name__ == "__main__":
    game = SetGame()
    game.play_self()
