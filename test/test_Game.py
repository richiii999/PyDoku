
from sys import path
path.append(".")

import Game
from copy import deepcopy

g1 = Game.SudokuGame(RNG=12)
print("Solution")
g1.prettyPrint(g1.solution)
print("Initial state")
g1.prettyPrint(info=True)

print("TEST: This is a mistake")
g1.PlaceTile(0,0,7)
g1.prettyPrint(g1.curr, info=True)

print("TEST: This is invalid, its in the initial state")
g1.PlaceTile(8,0,7)
g1.prettyPrint(g1.curr, info=True)

for row in range(9):
    for col in range(9):
        g1.PlaceTile(row,col,5)
g1.prettyPrint(g1.curr, info=True)

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

print("TEST: Solving board")
g1.curr = deepcopy(g1.solution)
g1.prettyPrint(info=True)
g1.PlaceTile(0,0,1) # Removing a tile
g1.PlaceTile(0,0,8) # Placing the final tile
# Should win here

#
