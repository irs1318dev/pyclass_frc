import os
import sys
import time

sys.path.append(os.path.dirname(__file__))

import tenthou.game as game


def main():
    """Top-level function for TenThosand dice game.
    
    This dice game is played from the command line. It is a two-
    player game with one human and one computer player.
    """
    
    # Introduction
    print("\n-----10000-----10000-----100000-----100000")
    name = input(f"Hello. My name is Ona. What's your name?.\n")
    print("Let's Play 10,000! I will go first.")
    time.sleep(0.5)
    print("This game will last 3 rounds. You can quit from any prompt by entering q.")
    print("I will go first.\n")
    time.sleep(1)

    # Setup and start game
    human_player = game.HumanPlayer(name)
    computer_player = game.ComputerPlayer("Ona")
    dicegame = game.Game(computer_player, human_player)
    dicegame.play()

if __name__ == "__main__":
    main()