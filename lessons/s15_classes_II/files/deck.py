# 1. Do not delete the %%writefile ... line. It must be the first line
#    the cell.
# 2. Create your Deck class in this cell.
# 3. Save the Deck class in the file deck.py by running this cell.
# 4. If you make changes to the class, re-run this cell to save
#    the changes to deck.py
import random

from card import Card
from pile import Pile

class Deck(Pile):
    def __init__(self):
        super().__init__()
        
        for suit in "cdhs":
            for rank in "a23456789tjqk":
                self.place_card(Card(suit=suit, rank=rank))
                
    def cut(self, loc=None):
        if loc is None:
            loc = random.randint(0, 51)
        elif loc < 0 or loc > 51:
            raise ValueError
        
        i = len(self) - loc
        self._cards = self._cards[i:] + self._cards[:i]
        
