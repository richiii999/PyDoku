
# Test the generator

from sys import path
path.append(".")

import Generator

numEmpty = 20 # Set the number of empty cells
sudokuSet = Generator.GenerateSudokuSet(numEmpty)

print("Initial State")
for row in sudokuSet[0]: print(" ".join(map(str, row)))

print("Solution")
for row in sudokuSet[1]: print(" ".join(map(str, row)))
