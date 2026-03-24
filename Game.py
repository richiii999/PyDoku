
# Game.py
# Stores the current game state and has functions to play the game

# TODO
# 1. init, curr, solution states saved
# 2. func to place a number in a square, it cannot be an init square
# 3. pretty print with | _ walls and . instead of 0

import Generator # Generate Sudoku initial and solution states
import Gamedata # Metadata struct

class SudokuGame:
    def __init__(self, difficulty = 40, RNG=None):

        # Board states
        states = Generator.GenerateSudokuSet(difficulty, RNG=RNG)
        self.initial = states[0]
        self.curr = states[0]
        self.solution = states[1]

        # Metadata
        self.gamedata = Gamedata.Gamedata()

    def prettyPrint(self, grid, wall='|', floor='-', empty='.'):
        """Prints the full Sudoku board with formatting"""

        for row in grid:
            if grid.index(row) != 0 and grid.index(row) % 3 == 0: print(f"{floor * 21}") # Horz separator
            txtRow = [N if N != 0 else empty for N in row]
            print(f"{txtRow[0]} {txtRow[1]} {txtRow[2]} {wall} {txtRow[3]} {txtRow[4]} {txtRow[5]} {wall} {txtRow[6]} {txtRow[7]} {txtRow[8]}")


# TESTING

g1 = SudokuGame(RNG=12)
g1.prettyPrint(g1.initial)
