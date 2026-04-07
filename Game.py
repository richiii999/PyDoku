
# Game.py
# Stores the current game state and has functions to play the game

import Generator # Generate Sudoku initial and solution states
from copy import deepcopy # Deepcopy the board since its nested lists
import numpy as np # Multi-dim arrays easily
from database.db_manager import db_function as db

class SudokuGame:
    def __init__(self,initial_map, curr,solution,notes, difficulty = 40, RNG=None):
        # Board states


        if initial_map == None:  
            self.newmapcreated = True     
            states = Generator.GenerateSudokuSet(difficulty, RNG=RNG)
            self.initial  = deepcopy(states[0])
            self.curr     = deepcopy(states[0])
            self.solution = deepcopy(states[1])

            self.notes = np.zeros((9,9,9), dtype='int')
        else:
            self.newmapcreated = False
            self.initial  = deepcopy(initial_map)
            self.curr     = deepcopy(curr)
            self.solution = deepcopy(solution)
            self.notes = notes

        # Metadata
        self.time = 0 # How long the game took (in sec)
        self.numMistakes = 0 # Num placements not in solution
        self.numNotes = 0 # Num notes added
        self.difficulty = 0 # Num empty squares started with

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
    ###TODO: FINISH TH ISSOLVED
    def check_then_close(self) -> None:
        """Stops the game and submits it to the database if won"""
        print("Win!")
        if not self.IsSolved(): raise RuntimeError("Tried to win an unsolved board!")

    def SubmitToDB(self, session_id) -> None:
        sess_id = session_id

        if self.newmapcreated == True:
           #adding new rows if created a new map
           new_id =  db.add_new_map(self.initial,self.solution,self.difficulty)
           sess_id = db.add_session(new_id,self.curr)
        

        #actual update the session with timestamps and update it's completion status fo rthis object
        db.save_session(session_id, self.curr, self.time, self.notes)
        db.update_completion_status(sess_id,self.IsSolved())






