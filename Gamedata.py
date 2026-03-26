
# Gamedata.py
# Defines the game metadata struct

import time

class Gamedata:
    def __init__(self, time=0, mistakes=0, notes=0, difficulty=0):
        self.time = time # How long the game took (in sec)
        self.numMistakes = mistakes # Num placements not in solution
        self.numNotes = notes # Num notes added
        self.difficulty = difficulty # Num empty squares started with
