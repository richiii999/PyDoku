
# Gamedata.py
# Defines the game metadata struct

import time

class Gamedata:
    def __init__(self):
        self.time = -1 # How long the game took (in sec)
        self.mistakes = -1 # Num placements not in solution
        self.notes = -1 # Num notes added
        self.difficulty = -1 # Num empty squares started with
