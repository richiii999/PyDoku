
''' how we can access the db test file'''


from db_manager import db_function as db

from sys import path
path.append("..")

import Generator

numEmpty = 20 # Set the number of empty cells
sudokuSet = Generator.GenerateSudokuSet(numEmpty)
new_map = db.array_to_string(sudokuSet[0])
solution = db.array_to_string(sudokuSet[1])


new_map_id = db.add_new_map(new_map,solution) #returns back it's id



'''



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

