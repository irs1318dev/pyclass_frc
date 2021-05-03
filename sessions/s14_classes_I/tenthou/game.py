import os
import sys
import time

sys.path.append(os.path.dirname(__file__))

import tenthou.dice as dice

class Player():
    def __init__(self, name):
        self.score = 0
        self.name = name


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def check_quit(self, user_input, turn):
        if user_input == "q":
            raise QuitError(turn.player.name)

    def decide_hotdice(self, turn):
        inp = input("Would you like to roll all 5 dice again? (y/n)").lower()
        self.check_quit(inp, turn)
        return inp == "y"

    def decide_end_turn(self, turn):
        inp = input("Do you want to end your turn now? (y/n)").lower()
        self.check_quit(inp, turn)
        return inp == "y"

    def decide_table(self, turn):
        prompt = ("Which dice would you like to table?"
                  "\nEnter single digit for each die, with no spaces, e.g 115.\n")
        inp = input(prompt)
        self.check_quit(inp, turn)
        return inp


class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def decide_hotdice(self, turn):
        return True

    def decide_end_turn(self, turn):
        unscored_dice = len(turn.rollable) - turn.rollable.scored_dice
        return unscored_dice < 3

    def decide_table(self, turn):
        roll = turn.rollable
        table = ["1"] * roll.ones
        table += ["5"] * roll.fives
        if roll.triple != 0:
            table += [str(roll.triple)] * 3
        return "".join(table)

class QuitError(Exception):
    pass


class Game():
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play(self):
        quit_early = False
        try:
            for num_round in range(1, 4):
                print("##### Beginning round", num_round, "###############")
                print(f"{self.player1.name}'s Score: {self.player1.score}",
                    f"\t{self.player2.name}'s Score: {self.player2.score}\n")

                turn = Game.Turn(self.player1, self.player2)
                self.player1.score += turn.do()
                turn = Game.Turn(self.player2, self.player1)
                self.player2.score += turn.do()
                time.sleep(2)
        except QuitError as q_error:
            print(q_error, "is ending the game.")
            quit_early = True

        print("Game Results!-------------")
        print(f"{self.player1.name}'s score:", self.player1.score)
        print(f"{self.player2.name}'s score:", self.player2.score)

        if not quit_early:
            if self.player1.score > self.player2.score:
                print(self.player1.name, "has won the game!")
            elif self.player1.score < self.player2.score:
                print(self.player2.name, "has won the game!")
            else:
                print("The game ended in a tie!")

    class Turn():
        def __init__(self, player, opponent):
            self.player = player
            self.opponent = opponent
            self.score = 0
            self.tabled_die = []
            self.rollable = dice.RollableDice()

        @property
        def tabled_die_str(self):
             return " || ".join([str(dice) for dice in self.tabled_die])

        def do(self):
            print(f"=====Starting {self.player.name}'s Turn.==========")
            while(True):
                # Show turn status
                if self.tabled_die:
                    print("Tabled Dice:", self.tabled_die_str, "\n")
                time.sleep(1)

                # Roll Dice
                print(f"Rolling {len(self.rollable)} dice!----------")
                self.rollable.roll()
                print(f"{self.player.name}'s roll:", self.rollable,
                      "\tDice Score:", self.rollable.score)
                time.sleep(2)

                # Zero Points -- Turn Over
                if self.rollable.score == 0:
                    print(self.player.name, "rolled zero points.",
                          f"{self.player.name}'s turn is over!!!")
                    self.score = 0
                    time.sleep(2)
                    break

                # Hot dice
                if self.rollable.scored_dice == len(self.rollable):
                    print(self.player.name, "has hot dice!")
                    print(f"{self.player.name}'s turn score is:",
                          self.score)
                    if self.player.decide_hotdice(self):
                        print(self.player.name, "is re-rolling all five dice!")
                        self.score += self.rollable.score
                        self.rollable = dice.RollableDice()
                        time.sleep(2)
                        continue

                # Table dice
                table = self.player.decide_table(self)
                removed_dice = self.rollable.remove_dice(table)
                while isinstance(removed_dice, str):
                    print(removed_dice)
                    table = self.player.decide_table(self)
                    removed_dice = self.rollable.remove_dice(table)

                tabled_dice = dice.Dice()
                tabled_dice.add_dice(removed_dice)
                self.tabled_die.append(tabled_dice)
                print(f"{self.player.name} is tabling these die:",
                        tabled_dice, "\tScore:", tabled_dice.score)
                self.score += tabled_dice.score
                print(f"{self.player.name}'s turn score:", self.score)
                print()

                # End turn
                if self.player.decide_end_turn(self):
                    print(f"{self.player.name} is stopping.")
                    time.sleep(2)
                    break   

            print(f"{self.player.name}'s score for this turn:", self.score)
            print()

            return self.score
