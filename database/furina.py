
''' this is just a testfile remove later '''

from bisect import insort # Used for inserting to lists in-order
from copy import deepcopy # Deepcopy the board since its nested lists
import numpy as np # Multi-dim arrays easily


from database.db_manager import db_function as db
import Generator as gen





import random


states = gen.GenerateSudokuSet(6, RNG=3)
initial  = deepcopy(states[0])
curr     = deepcopy(states[0]) 
solution = deepcopy(states[1])


for i in range(10):
    newid = db.add_new_map(initial,solution,i)
    print(newid)

for i in range(8):
    time = random.random()
    time = round(time,2)
    db.update_time(i,time)

'''
matrix = [
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]],
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]],
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]]
]

print("afterwords")
for row in matrix: print(" ".join(map(str, row)))

all_sessions = db.get_all_map_and_id()
map_ids = []
for row in all_sessions:
    map_ids.append(row[0])
print(map_ids)

sessions = db.get_session_id_and_map(1)  
session_id = []
for row in sessions:
    session_id.append(row[0])
print(session_id)


matrix = [
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]],
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]],
    [[1,2,3,4], [1,2,3,4], [1,2,3,4]]
]

print("afterwords")
for row in matrix: print(" ".join(map(str, row)))


db.update_notes(matrix)

notes = db.get_notes(1)
print("getback")
for row in notes: print(" ".join(map(str, row)))

matrix = db.convert_2d_to_3d(notes)
for row in matrix: print(" ".join(map(str, row)))


numEmpty = 20 # Set the number of empty cells
sudokuSet = Generator.GenerateSudokuSet(numEmpty)
new_map = db.array_to_string(sudokuSet[0])
solution = db.array_to_string(sudokuSet[1])


new_map_id = db.add_new_map(new_map,solution) #returns back it's id



solutionfromdb = db.get_solution_and_id(new_map_id)


print('from the db')
for row in mapfromdb[1]: print(" ".join(map(str, row)))
print('solution from db')
for row in solutionfromdb[1]: print(" ".join(map(str, row)))



print("Initial State")
for row in sudokuSet[0]: print(" ".join(map(str, row)))
new_map = db.array_to_string(sudokuSet[0])
print(new_map)
print("checkifconversionbackworks")
new_new_map = db.string_to_array(new_map)
for row in new_new_map: print(" ".join(map(str, row)))



print("Solution")
for row in sudokuSet[1]: print(" ".join(map(str, row)))
'''

#map = db

#print(map.get_all_map_and_id())

