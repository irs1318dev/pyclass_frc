# 1. Do not delete the %%writefile ... line. It must be the first line
#    the cell.
# 2. Create your Card class in this cell.
# 3. Save the Card class in the file card.py by running this cell.
# 4. If you make changes to the class, re-run this cell to save
#    the changes to card.py

class Card:
    def __init__(self, rank, suit):
        rank = rank.lower()
        suit = suit.lower()
        if rank not in "a123456789tjqk" or suit not in "cdhs":
            raise ValueError
        if len(rank) != 1 or len(suit) !=1:
            raise ValueError
        self._rank = rank
        self._suit = suit
        
    @property
    def rank(self):
        return self._rank
    
    @property
    def suit(self):
        return self._suit
    
    def __str__(self):
        return self._rank + self._suit      
