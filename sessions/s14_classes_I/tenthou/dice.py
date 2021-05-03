import random
import re

class Die():
    def __init__(self, val=None):
        if val is None:
            self.value = None
        elif isinstance(val, int) and val >= 1 and val <= 6:
            self.value = val
        else:
            raise ValueError(f"Incorrect Die Value: {val}")
    
    def roll(self):
        self.value = random.randint(1, 6)

    def __str__(self):
        return str(self.value)


class Dice():
    def __init__(self):
        self.dice = []
        self.counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    def add_die(self, die):
        self.dice.append(die)
        if die.value is not None:
            self.counts[die.value] += 1

    def add_dice(self, dice):
        for die in dice:
            self.add_die(die)

    @property
    def ones(self):
        return self.counts[1]

    @property
    def fives(self):
        return self.counts[5]

    @property
    def triple(self):
        for key, val in self.counts.items():
            if key not in [1, 5]:
                if val >= 3:
                    return key
        return 0
        
    @property
    def score(self):
        return (
            self.fives +
            2 * self.ones +
            (14 if self.ones >= 3 else 0) +
            (7 if self.fives >= 3 else 0) +
            2 * self.triple) * 50

    @property
    def scored_dice(self):
        return self.fives + self.ones + (3 if self.triple != 0 else 0)

    def __len__(self):
        return len(self.dice)

    def __str__(self):
        return " | ".join([str(die) for die in self.dice])



class RollableDice(Dice):

    def __init__(self, values=None, num_dice=5):
        super().__init__()

        if values is None:
            values = [None] * num_dice

        for val in values:
            self.add_die(Die(val))

    def roll(self):
        self.counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for die in self.dice:
            die.roll()
            self.counts[die.value] += 1

    def remove_dice(self, dice):
        # Check that dice contains only digits 1 - 6
        if re.fullmatch(r"[1-6]{1,5}", dice) is None:
            return "Invalid Input. Enter up to five digits 1 through 6."
        # Check that all dice were present in roll and scorable
        for val in range(1, 7):
            if dice.count(str(val)) > self.counts[val]:
                return f"You entered too many {val}'s."
        # Check that exactly three die entered for die not 1 or 5.
        for die_val in dice:
            if die_val not in ["1", "5"] and dice.count(die_val) != 3:
                return f"You must table exactly three {die_val}'s."

        removed_dice = []
        for die_val in dice:
            for idx, die in enumerate(self.dice):
                if die.value == int(die_val):
                    removed_dice.append(die)
                    del self.dice[idx]
                    self.counts[int(die_val)] -= 1
                    break
        return removed_dice



        



