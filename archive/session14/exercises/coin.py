import random

class Coin:
    """This is a docstring."""
    values = {"penny": 1, "nickle": 5, "dime": 10, "quarter": 25}
    
    def __init__(self, coin_type, up=None):
        """This is also a docstring"""
        
        if coin_type in Coin.values.keys():
            self.coin_type = coin_type
        else:
            raise ValueError(f"coin_type must be in {Coin.values.keys()}")
            
        if up is not None:
            self.up_side = up
        else:
            self.up_side = None
            
        self.cents = Coin.values[self.coin_type]
            

            
    def flip(self):
        self.up_side = random.choice(["heads", "tails"])
        
    def _cents(self, val):
        return val.cents if isinstance(val, Coin) else val
        
    def __add__(self, other):
        if isinstance(other, Coin):
            return self.cents + other.cents
        else:
            return self.cents + other
        
    def __radd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError
        else:
            return other * self.cents
            
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __eq__(self, other):
        return self.cents == self._cents(other)
    
    def __ne__(self, other):
        return self.cents != self._cents(other)
    
    def __lt__(self, other):
        return self.cents < self._cents(other)
    
    def __le__(self, other):
        return self.cents <= self._cents(other)
    
    def __gt__(self, other):
        return self.cents > self._cents(other)
    
    def __ge__(self, other):
        return self.cents >= self._cents(other)
    
    def __str__(self):
        return str(self.cents)
    