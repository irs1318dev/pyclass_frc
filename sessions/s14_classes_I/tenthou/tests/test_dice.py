import os
import re
import sys

import pytest

# Get path to parent folder and add to system path
par_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(par_folder)

import tenthou.dice as dice

def test_die():
    die = dice.Die()
    assert die.value is None

    die.roll()
    assert isinstance(die.value, int)
    assert die.value >= 1 and die.value <= 6

    for val in range(1, 7):
        die = dice.Die(val)
        assert die.value == val
        assert str(die) == str(val)

    with pytest.raises(ValueError) as verror:
        dice.Die(0)
    assert "Incorrect Die Value: 0" in str(verror)



def test_dice():
    dices = dice.Dice()
    assert len(dices) == 0
    assert str(dices) == ''
    for val in [1, 1, 1, 1, 1]:
        dices.add_die(dice.Die(val))

    assert dices.ones == 5
    assert dices.fives == 0
    assert dices.triple == 0
    assert len(dices) == 5
    assert str(dices) == "1 | 1 | 1 | 1 | 1"
    assert dices.score == 1200

    dices = dice.Dice()
    for val in [2, 2, 2, 1, 5]:
        dices.add_die(dice.Die(val))
    assert dices.ones == 1
    assert dices.fives == 1
    assert dices.triple == 2
    assert dices.score == 350
    assert str(dices) == "2 | 2 | 2 | 1 | 5"
    assert dices.scored_dice == 5

def test_rollable():

    roll = dice.RollableDice([3, 6, 6, 6, 3])
    assert roll.ones == 0
    assert roll.fives == 0
    assert roll.triple == 6
    assert roll.score == 600
    assert str(roll) == "3 | 6 | 6 | 6 | 3"
    assert roll.scored_dice == 3

    assert len(roll) == 5
    rem_dice = roll.remove_dice("666")
    assert len(roll) == 2
    tabled_dice = dice.Dice()
    tabled_dice.add_dice(rem_dice)
    assert(len(tabled_dice)) == 3
    assert str(tabled_dice) == "6 | 6 | 6"
    assert str(roll) == "3 | 3"
    assert tabled_dice.score == 600
    assert roll.score == 0

    roll = dice.RollableDice()
    assert str(roll) == "None | None | None | None | None"
    roll.roll()
    ptn = re.compile(r"[1-6] \| [1-6] \| [1-6] \| [1-6] \| [1-6]")
    assert ptn.fullmatch(str(roll)) is not None
