import os
import sys
import time

sys.path.append(os.path.dirname(__file__))

import tenthou.dice as dice

class Player():
    """A player for the dice game TenThousand.
    
    Attributes:
        score: a positive integer.
        name: string, the player's name.
        
    Instantiation:
        `player = Player("player's name")`
    """
    def __init__(self, name):
        self.score = 0
        self.name = name


class HumanPlayer(Player):
    """A human player. Inherits from Player class.
    
    Human player decisions are made by getting user
    input from the command line.
    """
    def __init__(self, name):
        super().__init__(name)

    def check_quit(self, user_input, turn):
        """Determines if player wants to quit early.
        
        Args:
            user_input: string, input from command line.
            turn: 
        
        Raises:
            QuitError if user enters "q" when prompted to quit.
        """
        if user_input == "q":
            raise QuitError(turn.player.name)

    def decide_hotdice(self, turn):
        """Decide whether to reroll all hot dice.
        
        Args:
            turn: A game.Turn object representing the current
                player's turn.
                
        Returns: Boolean
        """
        inp = input("Would you like to roll all 5 dice again? (y/n)").lower()
        self.check_quit(inp, turn)
        return inp == "y"

    def decide_end_turn(self, turn):
        """Decide whether to end a turn
        
        Args:
            turn: A game. Turn object representing the current
                player's turn.
                
        Returns: Boolean
        """
        inp = input("Do you want to end your turn now? (y/n)").lower()
        self.check_quit(inp, turn)
        return inp == "y"

    def decide_table(self, turn):
        """Decide which dice to table.
        
        Args:
            turn: A game. Turn object representing the current
                player's turn.
                
        Returns: string, numbers of dice that should be tabled. All
            die represented with a single integer, 1 through 6. There
            are no spaces between multiple die.
        """
        prompt = ("Which dice would you like to table?\n"
                  "Enter single digit for each die, with no spaces, e.g 115.\n"
                  "Enter a hyphen ('-') to table zero dice.\n")
        inp = input(prompt)
        self.check_quit(inp, turn)
        return inp


class ComputerPlayer(Player):
    """A computer player. Inherits from Player class.
    
    Computer player decisions are made using simple
    rules.
    """
    
    def __init__(self, name):
        super().__init__(name)
    
    def decide_hotdice(self, turn):
        """Decide whether to reroll all hot dice.
        
        The comptuer always rerolls hot dice, so this method always
        returns True.
        
        Args:
            turn: A game.Turn object representing the current
                player's turn.
                
        Returns: Boolean
        """
        return True

    def decide_end_turn(self, turn):
        """Decide whether to end a turn
        
        The computer always ends the turn if there are two or
        fewer dice to roll.
        
        Args:
            turn: A game. Turn object representing the current
                player's turn.
                
        Returns: Boolean
        """
        unscored_dice = len(turn.rollable) - turn.rollable.scored_dice
        return unscored_dice < 3

    def decide_table(self, turn):
        """Decide which dice to table.
        
        Args:
            turn: A game. Turn object representing the current
                player's turn.
                
        Returns: string, numbers of dice that should be tabled. All
            die represented with a single integer, 1 through 6. There
            are no spaces between multiple die.
        """
        roll = turn.rollable
        table = ["1"] * roll.ones
        table += ["5"] * roll.fives
        if roll.triple != 0:
            table += [str(roll.triple)] * 3
        return "".join(table)

    
class QuitError(Exception):
    """Thrown when a player decides to quit."""
    pass


class Game():
    """A single game of TenThousand.
    
    Attributes:
        player1: A ComputerPlayer or HumanPlayer object.
        player2: A ComputerPlayer or HumanPlayer object.
    """
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play(self):
        """Play a single game of TenThousand.
        """
        quit_early = False
        try:
            # Play three rounds, unless Human player quits early.
            for num_round in range(1, 4):
                self.play_round(num_round, 2)
                
        # Executed if human player quits early
        except QuitError as q_error:
            print(q_error, "is ending the game.")
            quit_early = True
            
        # Display end-of-game information.
        self.end_game(quit_early)

    def play_round(self, num_round, sleep):
        """Play a single round of TenThousand.
        
        A round consistes of one turn for each player.
        """
        print("##### Beginning round", num_round, "###############")
        print(f"{self.player1.name}'s Score: {self.player1.score}",
            f"\t{self.player2.name}'s Score: {self.player2.score}\n")
        
        # Player 1's turn
        turn = Game.Turn(self.player1, self.player2)
        self.player1.score += turn.do()
        
        # Player 2's turn
        turn = Game.Turn(self.player2, self.player1)
        self.player2.score += turn.do()
        
        # Keep text from scrolling too fast on CLI.
        time.sleep(sleep)

    def end_game(self, quit_early):
        """Displays end-of-game info.
        
        Args:
            quit_early: Boolean. True of user requested to
                quit before finishing three turns.        
        """
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
        """A single turn for a single player.

        Attributes:
            player: A game.HumanPlayer or game.ComputerPlayer object
                representing the player whose turn it is.
            player: A game.HumanPlayer or game.ComputerPlayer object
                representing the player whose turn it is not.
            score: integer, score from current turn.
            tabled_die: list of dice.Die objects.
            tabled_die_str: sting showing all tabled die.
            rollable: Set of five dice.                
        """
        def __init__(self, player, opponent):
            """
            Args:
                player: A game.HumanPlayer or game.ComputerPlayer object
                    representing the player whose turn it is.
                player: A game.HumanPlayer or game.ComputerPlayer object
                    representing the player whose turn it is not.
            """
            self.player = player
            self.opponent = opponent
            self.score = 0
            self.tabled_die = []
            self.rollable = dice.RollableDice()

        def do(self):
            """Executes a single turn.
            """
            print(f"=====Starting {self.player.name}'s Turn.==========")
            while(True):
                self.show_tabled_die(1)
                self.roll_die(2)

                # Turn ends if no points were rolled
                if self.check_zero_points(2):
                    break

                # See if player wants to reroll after hot dice.
                if self.check_hotdice_reroll(2):
                    continue

                # Get additional tabled dice.
                self.tabled_die.append(self.get_tabled_dice())

                # Check if player wants to end turn.
                if self.check_end_turn(2):
                    break

            # Print end of turn info
            print(f"{self.player.name}'s score for this turn:", self.score)
            print()
            return self.score

        @property
        def tabled_die_str(self):
            """Gets string containing tabled dice."""
            return " || ".join([str(dice) for dice in self.tabled_die])

        def show_tabled_die(self, sleep):
            """Display tabled die.

            Args:
                sleep: integer, Number of seconds to pause after
                    showing output.
            """
            if self.tabled_die:
                print("Tabled Dice:", self.tabled_die_str, "\n")
            time.sleep(sleep)

        def roll_die(self, sleep):
            """Roll dice.

            Args:
                sleep: integer, Number of seconds to pause after
                    showing output.
            """
            print(f"Rolling {len(self.rollable)} dice!----------")
            self.rollable.roll()
            print(f"{self.player.name}'s roll:", self.rollable,
                    "\tDice Score:", self.rollable.score)
            time.sleep(sleep)

        def check_zero_points(self, sleep):
            """Check if zero points were scored.

            Args:
                sleep: integer, Number of seconds to pause after
                    showing output.

            Returns: Boolean
            """
            zero_points = self.rollable.score == 0
            if zero_points:
                print(self.player.name, "rolled zero points.",
                      f"{self.player.name}'s turn is over!!!")
                self.score = 0
                time.sleep(sleep)
            return zero_points

        def check_hotdice_reroll(self, sleep):
            """Check if player has hotdice and wants to reroll.

            Returns: Boolean.
            """
            reroll_hotdice = False
            if self.rollable.scored_dice == len(self.rollable):
                print(self.player.name, "has hot dice!")
                print(f"{self.player.name}'s turn score is:",
                        self.score)
                if self.player.decide_hotdice(self):
                    reroll_hotdice = True
                    print(self.player.name, "is re-rolling all five dice!")
                    self.score += self.rollable.score
                    self.rollable = dice.RollableDice()
                    time.sleep(sleep)
            return reroll_hotdice

        def get_tabled_dice(self):
            """Get tabled dice.

            Returns: list of Die objects.
            """
            table = self.player.decide_table(self)
            removed_dice = self.rollable.remove_dice(table)
            while isinstance(removed_dice, str):
                print(removed_dice)
                table = self.player.decide_table(self)
                removed_dice = self.rollable.remove_dice(table)
            tabled_dice = dice.Dice()
            tabled_dice.add_dice(removed_dice)
            print(f"{self.player.name} is tabling these die:",
                    tabled_dice, "\tScore:", tabled_dice.score)
            self.score += tabled_dice.score
            return tabled_dice

        def check_end_turn(self, sleep):
            """Check if player wants to end their turn.

            Returns: Boolean
            """
            print(f"{self.player.name}'s turn score:", self.score)
            print()
            end_turn = False
            if self.player.decide_end_turn(self):
                print(f"{self.player.name} is stopping.")
                time.sleep(sleep)
                end_turn = True
            return end_turn
