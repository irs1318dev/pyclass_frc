import random

class DieTestable:
    def __init__(self, val=None):
        if val is None:
            self.roll()
        else:
            self.value = val
        
    def roll(self):
        self.value = random.randint(1, 6)
