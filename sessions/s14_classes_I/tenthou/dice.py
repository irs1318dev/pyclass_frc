import random
import re

class Die():
    """A single six-sided die.
    
    Attributes:
        value: An integer between 1 and 6 inclusive.
        roll(): Assigns a random integer to the value attribute,
            between 1 and 6 inclusive.
    """
    def __init__(self, val=None):
        """Constructor for a six-sided die.
        
        Args:
            val: Optional. Accepts an integer value between 1
                6 inclusive, which becomes the die's initial value.
                If omitted, a random integer is assigned.
                
        Raises:
            ValueError if val is an integer but not between 1 and 6.
            TypeError if val is not an integer.
        """
        if val is None:
            self.roll()
            # print("rolling die!!!!!")
        elif not isinstance(val, int):
            raise TypeError(f"val is not an integer: {type(val)}")
        elif val < 1 or val > 6:
            raise ValueError(f"val not between 1 and 6: {val}")
        else:
            self.value = val
    
    def roll(self):
        """Rolls the die, generating a new random value from 1 to 6.
        """
        self.value = random.randint(1, 6)

    def __str__(self):
        """Causes print() and str() to show the die's value.
        """
        return str(self.value)


class Dice():
    """A group of dice used to play Ten Thousand.
    
    This class is used both for tabled and untabled dice.
    
    Attributes:
        __init__(): Takes no arguments.
        add_die(): Adds a die to the group.
        add_dice(): Adds a list of dice to the group.
        ones: The number of die that have value 1.
        fives: The number of die that have value 5.
        triple: Indicates if there are three or more die with
            value 2, 3, 4, or 6.
        score: The score, counting all dice.
        scored_dice: The number of dice that score points.
        counts: dict, number of dice with each value.
            Has keys 1 - 6.
    """
    def __init__(self):
        """Constructs a new Dice object.
        """
        self.dice = []
        # Tracks how many dice have each value.
        self._counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    def add_die(self, die):
        """Adds a single die to the Dice.
        
        Args:
            die: A tenthou.dice.Die object.
        """
        self.dice.append(die)
        if die.value is not None:
            self._counts[die.value] += 1

    def add_dice(self, dice):
        """Adds a list of dice to the Dice object.
        
        Args:
            dice: A Python list of tenthou.dice.Die objects.
        """
        for die in dice:
            self.add_die(die)

    @property
    def ones(self):
        """The number of dice with value 1."""
        return self._counts[1]

    @property
    def fives(self):
        """The number of dice with value 5."""
        return self._counts[5]

    @property
    def triple(self):
        """Indicates if there are 3 or more die with the same value.
        
        The possible values are 0, 2, 3, 4, and 6. The die with value
        1 or 5 have no impact on this property. Use the ones or fives
        properties to see how many 1 or 5 die are in the group. If 0,
        there are no triples. If 2, then there is are three or more die
        with value 2. If 3, there are three or more die with value 3,
        etc.
        """
        for key, val in self._counts.items():
            if key not in [1, 5]:
                if val >= 3:
                    return key
        return 0
        
    @property
    def score(self):
        """The points available from 1s, 5s, and triples."""
        return (
            self.fives +
            2 * self.ones +
            (14 if self.ones >= 3 else 0) +
            (7 if self.fives >= 3 else 0) +
            2 * self.triple) * 50

    @property
    def scored_dice(self):
        """The number of dice that score points.
        """
        return self.fives + self.ones + (3 if self.triple != 0 else 0)

    def __len__(self):
        """Number of dice in set."""
        return len(self.dice)

    def __str__(self):
        """String showing values of all dice in set."""
        return " | ".join([str(die) for die in self.dice])



class RollableDice(Dice):
    """The untabled dice used in the game TenThousand.
    
    Inherits from Dice class.
    
    Unatabled dice can still be rolled. Therefore this class
    contains a method for rolling the dice.
    """

    def __init__(self, values=None, num_dice=5):
        """Initialized a RollableDice object.
        
        Args:
            values: [integer], list of dice values.
            num_dice: integer, number of dice in set.
        """
        super().__init__()

        if values is None:
            values = [None] * num_dice

        for val in values:
            self.add_die(Die(val))

    def roll(self):
        """Roll all dice in set.
        
        Assigns a random number, 1 - 6, to each die in set.
        """
        self._counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for die in self.dice:
            die.roll()
            self._counts[die.value] += 1

    def remove_dice(self, dice):
        """Removes dice from set. Used for tabling dice.
        
        Args:
            dice: string, contains integers 1 - 6 representing
                dice that should be removed.
                
        Returns: list of removed Die objects.
        """
        # Check if no dice are to be removed
        if dice == "-":
            return []
        # Check that dice contains only digits 1 - 6
        if re.fullmatch(r"[1-6]{1,5}", dice) is None:
            return "Invalid Input. Enter up to five digits 1 through 6."
        # Check that all dice were present in roll and scorable
        for val in range(1, 7):
            if dice.count(str(val)) > self._counts[val]:
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
                    self._counts[int(die_val)] -= 1
                    break
        return removed_dice



        



