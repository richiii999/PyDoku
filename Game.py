
# Game.py
# Stores the current game state and has functions to play the game

import Generator # Generate Sudoku initial and solution states
from copy import deepcopy # Deepcopy the board since its nested lists
import numpy as np # Multi-dim arrays easily

class SudokuGame:
    def __init__(self, initial=None, curr=None, solution=None, notes=None, time=0, numMistakes=0, numNotes=0, difficulty=40, RNG=None):

        # Board states
        states = Generator.GenerateSudokuSet(difficulty, RNG=RNG)
        self.initial  = (initial  is not None) ? initial  : deepcopy(states[0])
        self.curr     = (curr     is not None) ? curr     : deepcopy(states[0])
        self.solution = (solution is not None) ? solution : deepcopy(states[1])

        self.notes = (notes is not None) ? notes : np.zeros((9,9,9), dtype='int')

        # Metadata
        self.time        = time # How long the game took (in sec)
        self.numMistakes = numMistakes # Num placements not in solution
        self.numNotes    = numNotes # Num notes added
        self.difficulty  = difficulty # Num empty squares started with

    def prettyPrint(self, grid=None, wall='|', floor='-', empty='.', info=False) -> None:
        """Prints the full Sudoku board with formatting"""
        if grid is None: grid = self.curr

        for row in grid:
            if grid.index(row) != 0 and grid.index(row) % 3 == 0: print(f"{floor * 21}") # Horz separator
            txtRow = [N if N != 0 else empty for N in row]
            print(f"{txtRow[0]} {txtRow[1]} {txtRow[2]} {wall} {txtRow[3]} {txtRow[4]} {txtRow[5]} {wall} {txtRow[6]} {txtRow[7]} {txtRow[8]}")

        if info:
            print(f"Mistakes={self.numMistakes}, Notes={self.numNotes}\n")

    def PlaceTile(self, row, col, val) -> None:
        """Attempts to place val at [row][col]"""
        if row < 0 or row > 8: raise ValueError("Invalid row")
        if col < 0 or col > 8: raise ValueError("Invalid col")
        if val < 1 or val > 9: raise ValueError("Invalid val")

        print(f"Placing {val} @ {row},{col}")

        if self.initial[row][col] != 0:
            print("Tile in initial state, ignoring tile")
            return

        elif val == self.curr[row][col]:
            print("Duplicate, removing tile")
            self.curr[row][col] = 0
            return

        if val != 0 and not self.solution[row][col] == val:
            self.numMistakes += 1

        self.curr[row][col] = val

        if self.IsSolved(): self.SubmitToDB()


    def AddNote(self, row, col, val) -> None:
        """Attempts to place val at [row][col]"""
        if row < 0 or row > 8: raise ValueError("Invalid row")
        if col < 0 or col > 8: raise ValueError("Invalid col")
        if val < 1 or val > 9: raise ValueError("Invalid val")

        print(f"Noting {val} @ {row},{col}")

        if self.initial[row][col] != 0:
            print("Tile in initial state, ignoring note")

        elif val == self.notes[row][col][val-1]:
            print("Duplicate, removing note")
            self.notes[row][col][val-1] = 0

        else:
            self.notes[row][col][val-1] = val
            self.numNotes += 1

    def IsSolved(self) -> bool:
        """Returns T/F if board is solved"""
        return self.curr == self.solution


    def SubmitToDB(self) -> None:
        """Stops the game and submits it to the database if won"""
        print("Win!")
        if not self.IsSolved(): raise RuntimeError("Tried to win an unsolved board!")

        # TODO
        # Stop timer
        # Save metadata to DB

        ##FUNCITONS WE NEED DONE
#####TODO: FINISH THE SAVE SESION FUNCTIONS
#### TODO: RUN SESSION aka pull a session id from list and then call that session info from the db
####TODO: GET PREVIOUS SESSION LIST MAKE SURE THE STATUS IS THERE so a list of session_ids and their completion status

