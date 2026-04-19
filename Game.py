
### Game.py
# Stores the current game state and has functions to play the game

from copy import deepcopy # Deepcopy the board since its nested lists
import numpy as np # Multi-dim arrays easily

import Generator # Generate Sudoku initial and solution states
from database.db_manager import db_function as db

import logging

logging.basicConfig(
    level=logging.INFO,
    filename='pydoku.log',
    filemode='a',
    format='%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S',
)

logger = logging.getLogger(__name__)

class SudokuGame:
    def __init__(self, initial=None, curr=None, solution=None, notes=None, time=0, numMistakes=0, numNotes=0, difficulty=40, RNG=None, ID=0):
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        
        # Board states - generate only if not loading 
        if initial is None or solution is None:
            states = Generator.GenerateSudokuSet(difficulty, RNG=RNG)
            self.initial = deepcopy(states[0])  # Initial values cannot be changed
            self.solution = deepcopy(states[1]) # Solution to check mistakes against
        else:
            self.initial = deepcopy(initial)
            self.solution = deepcopy(solution)
        
        self.curr = deepcopy(self.initial) if curr is None else deepcopy(curr) # At the start, curr is just initial    

        self.notes = notes if (notes is not None) else np.zeros((9,9,9), dtype='int') # 3D Grid of 0's

        # Metadata
        self.time        = time        # How long the game took (in sec)
        self.numMistakes = numMistakes # Num placements not in solution
        self.numNotes    = numNotes    # Num notes added
        self.difficulty  = difficulty  # Num empty squares started with

        self.manual_save = False
        self.logger.info(f"Sol=\n{self.solution}")
        if ID != 0:
            self.ID = ID  # Loading a previous game, session already exists
            self.is_new = False # Signal if this is a new or old game to PyDoku
        else:
            map_id = db.add_new_map(self.initial, self.solution, self.difficulty)
            db.add_session(map_id, self.curr)  # create the session row
            # get the new session id that was just created
            self.ID = db.get_all_sessions_ids()[-1][0]
            self.is_new = True # Signal if this is a new or old game to pyDoku


        # Debug print the solution
        print("   --- SOLUTION ---")
        self.prettyPrint(self.solution, showMetadata=True)

    def prettyPrint(self, grid=None, wall='|', floor='-', empty='.', showMetadata=False) -> None:
        """Prints the Sudoku board with formatting"""
        if grid is None: grid = self.curr

        for row in grid: # Print each row of numbers with separators: 1 2 3 | 4 5 6 | 7 8 9
            if grid.index(row) != 0 and grid.index(row) % 3 == 0: print(f"{floor * 21}") # Horz separator every 3 lines
            txtRow = [N if N != 0 else empty for N in row]
            print(f"{txtRow[0]} {txtRow[1]} {txtRow[2]} {wall} {txtRow[3]} {txtRow[4]} {txtRow[5]} {wall} {txtRow[6]} {txtRow[7]} {txtRow[8]}")

        if showMetadata: # Optionally show the metadata for the game
            print(f"ID={self.ID}, Time={self.time}, Difficulty={self.difficulty}\nMistakes={self.numMistakes}, Notes={self.numNotes}\n")

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
            print("Mistake")
            self.numMistakes += 1

        self.curr[row][col] = val

        # Automatically submit finished game upon placing the last tile
        if self.IsSolved(): self.SubmitToDB(self.ID)

    def AddNote(self, row, col, val) -> None:
        """Attempts to place val at [row][col]"""
        if row < 0 or row > 8: raise ValueError("Invalid row")
        if col < 0 or col > 8: raise ValueError("Invalid col")
        if val < 1 or val > 9: raise ValueError("Invalid val")

        self.logger.info(f"Noting {val} @ {row},{col}")

        if self.initial[row][col] != 0:
            self.logger.info("Tile in initial state, ignoring note")

        elif val == self.notes[row][col][val-1]:
            self.logger.info("Duplicate, removing note")
            self.notes[row][col][val-1] = 0

        else: # Note is valid
            self.notes[row][col][val-1] = val
            self.numNotes += 1

    def IsSolved(self) -> bool:
        """Returns T/F if board is solved"""
        return self.curr == self.solution

    def SubmitToDB(self, session_id) -> None:
        """Submits the game's state to the DB, adding a new entry if needed"""
        sess_id = session_id

        if not db.ID_exists(sess_id): # If new game, create a new db entry
           new_id =  db.add_new_map(self.initial,self.solution,self.difficulty)
           sess_id = db.add_session(new_id,self.curr)


        # Update the session with curr timestamp & completion status
        try:
            db.save_session(session_id, self.curr, self.time, self.notes)
            db.update_completion_status(sess_id,self.IsSolved())
            self.logger.info(f"Session: {sess_id} has been updated")
        except Exception as e:
            self.logger.error("Unexpected Error: {e}")

    def SaveGame(self) -> None:
        """Interface for db.save_session()"""
        self.logger.info("Saving current game...")
        db.save_session(self.ID, self.curr, self.time, self.notes)
