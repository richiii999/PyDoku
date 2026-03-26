
# Game.py
# Stores the current game state and has functions to play the game

# TODO
# 1. init, curr, solution states saved
# 2. func to place a number in a square, it cannot be an init square
# 3. pretty print with | _ walls and . instead of 0

from copy import deepcopy

import Generator # Generate Sudoku initial and solution states
import Gamedata # Metadata struct

class SudokuGame:
    def __init__(self, difficulty = 40, RNG=None):

        # Board states
        states = Generator.GenerateSudokuSet(difficulty, RNG=RNG)
        self.initial = deepcopy(states[0])
        self.curr = states[0]
        self.solution = states[1]

        # Metadata
        self.meta = Gamedata.Gamedata(difficulty=difficulty)

    def prettyPrint(self, grid, wall='|', floor='-', empty='.', info=False):
        """Prints the full Sudoku board with formatting"""

        for row in grid:
            if grid.index(row) != 0 and grid.index(row) % 3 == 0: print(f"{floor * 21}") # Horz separator
            txtRow = [N if N != 0 else empty for N in row]
            print(f"{txtRow[0]} {txtRow[1]} {txtRow[2]} {wall} {txtRow[3]} {txtRow[4]} {txtRow[5]} {wall} {txtRow[6]} {txtRow[7]} {txtRow[8]}")

        if info:
            print(f"Mistakes={self.meta.mistakes}, Notes={self.meta.notes}\n")

    def PlaceTile(self, row, col, val):
        """Attempts to place val at [row][col]"""
        if row < 0 or row > 8: raise ValueError("Invalid row")
        if col < 0 or col > 8: raise ValueError("Invalid col")
        if val < 0 or val > 9: raise ValueError("Invalid val")

        print(f"Placing {val} @ {row},{col}")

        if self.initial[row][col] != 0:
            print("Tile in initial state, ignoring placement")
            return

        self.curr[row][col] = val

        if val != 0 and not self.solution[row][col] == val:
            self.meta.mistakes += 1

# TESTING

g1 = SudokuGame(RNG=12)
print("Solution")
g1.prettyPrint(g1.solution)
print("Initial state")
g1.prettyPrint(g1.curr, info=True)

print("TEST: This is a mistake")
g1.PlaceTile(0,0,7)
g1.prettyPrint(g1.curr, info=True)

print("TEST: This is invalid, its in the initial state")
g1.PlaceTile(8,0,7)
g1.prettyPrint(g1.curr, info=True)

# for row in range(9):
#     for col in range(9):
#         g1.PlaceTile(row,col,5)
# g1.prettyPrint(g1.curr, info=True)
