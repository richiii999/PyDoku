
# Game.py
# Stores the current game state and has functions to play the game

from copy import deepcopy

import Generator # Generate Sudoku initial and solution states
import Gamedata # Metadata struct
from bisect import insort # Used for inserting to lists in-order
from copy import deepcopy

class SudokuGame:
    def __init__(self, difficulty = 40, RNG=None):

        # Board states
        states = Generator.GenerateSudokuSet(difficulty, RNG=RNG)
        self.initial = deepcopy(states[0])
        self.curr = states[0]
        self.solution = states[1]
        self.notes = [ [ [] for _ in range(9) ] for _ in range(9)] 
        # Notes structure kinda bloated tbh

        # Metadata
        self.meta = Gamedata.Gamedata(difficulty=difficulty)

    def prettyPrint(self, grid=None, wall='|', floor='-', empty='.', info=False) -> None:
        """Prints the full Sudoku board with formatting"""
        if grid is None: grid = self.curr
        
        for row in grid:
            if grid.index(row) != 0 and grid.index(row) % 3 == 0: print(f"{floor * 21}") # Horz separator
            txtRow = [N if N != 0 else empty for N in row]
            print(f"{txtRow[0]} {txtRow[1]} {txtRow[2]} {wall} {txtRow[3]} {txtRow[4]} {txtRow[5]} {wall} {txtRow[6]} {txtRow[7]} {txtRow[8]}")

        if info:
            print(f"Mistakes={self.meta.numMistakes}, Notes={self.meta.numNotes}\n")

    def PlaceTile(self, row, col, val) -> None:
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
            self.meta.numMistakes += 1

    def AddNote(self, row, col, val) -> None:
        """Attempts to place val at [row][col]"""
        if row < 0 or row > 8: raise ValueError("Invalid row")
        if col < 0 or col > 8: raise ValueError("Invalid col")
        if val < 1 or val > 9: raise ValueError("Invalid val")

        print(f"Noting {val} @ {row},{col}")

        if self.initial[row][col] != 0:
            print("Tile in initial state, ignoring note")

        elif val in self.notes[row][col]:
            print("Duplicate, removing note")
            self.notes[row][col].remove(val)

        else: 
            insort(self.notes[row][col], val) # Insert in-order
            self.meta.numNotes += 1

    def CheckIfWin(self) -> bool:
        """Returns T/F if board is solved"""
        return self.curr == self.solution
    

# TESTING

g1 = SudokuGame(RNG=12)
print("Solution")
g1.prettyPrint(g1.solution)
print("Initial state")
g1.prettyPrint(info=True)

# print("TEST: This is a mistake")
# g1.PlaceTile(0,0,7)
# g1.prettyPrint(g1.curr, info=True)
# 
# print("TEST: This is invalid, its in the initial state")
# g1.PlaceTile(8,0,7)
# g1.prettyPrint(g1.curr, info=True)

# for row in range(9):
#     for col in range(9):
#         g1.PlaceTile(row,col,5)
# g1.prettyPrint(g1.curr, info=True)

print("TEST: Noting 3 values, there should be 81 slots for notes total, only 1 has notes")
g1.AddNote(0,1,3)
g1.AddNote(0,1,1)
g1.AddNote(0,1,2)
g1.prettyPrint(info=True)
print(g1.notes)
total=0
for i in g1.notes:
    for j in i:
            total += 1
print(f"Slots={total}")
