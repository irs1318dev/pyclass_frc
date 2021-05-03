import os
import sys

import pytest

# Get path to parent folder and add to system path
par_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(par_folder)

import tenthou.game as game
import tenthou.dice as dice

def test_player():
    plyr = game.Player("Stan")
    plyr.name == "Stan"
    plyr.score == 0

def test_computer_player():
    fiza = game.ComputerPlayer("Fiza")
    ona = game.ComputerPlayer("Ona")
    turn = game.Game.Turn(fiza, ona)

    turn.rollable = dice.RollableDice([2, 3, 4, 3, 2])
    assert not fiza.decide_end_turn(turn)
    assert fiza.decide_table(turn) == ""

    turn.rollable = dice.RollableDice([1, 1, 2, 3, 4])
    assert not fiza.decide_end_turn(turn)
    assert fiza.decide_table(turn) == "11"

    turn.rollable = dice.RollableDice([1, 1, 1, 2, 3])
    assert fiza.decide_end_turn(turn)
    assert fiza.decide_table(turn) == "111"

    turn.rollable = dice.RollableDice([2, 3])
    assert fiza.decide_end_turn(turn)
    assert fiza.decide_table(turn) == ""

    turn.rollable = dice.RollableDice([3, 3, 3, 1, 1])
    assert fiza.decide_hotdice(turn)
    assert fiza.decide_table(turn) == "11333"

