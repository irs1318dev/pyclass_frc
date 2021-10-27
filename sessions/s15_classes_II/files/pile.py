# 1. Do not delete the %%writefile ... line. It must be the first line
#    the cell.
# 2. Create your Pile class in this cell.
# 3. Save the Card class in the file card.py by running this cell.
# 4. If you make changes to the class, re-run this cell to save
#    the changes to card.py

import random

from card import Card

class Pile:
    def __init__(self):
        self._cards = []
        
    def __len__(self):
        return  len(self._cards)
    
    def place_card(self, card):
        if isinstance(card, Card):
            self._cards.append(card)
        else:
            raise ValueError
            
    def draw_card(self):
        return self._cards.pop()
    
    def __str__(self):
        return " | ".join([str(card) for card in self._cards[::-1]])
    
    def __getitem__(self, i):
        return self._cards[len(self) - 1 - i]
    
    def shuffle(self):
        random.shuffle(self._cards)
            
