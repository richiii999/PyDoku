
# Generator.py
# Generates a Sudoku initial state and solution.
# Adapted from: https://www.geeksforgeeks.org/dsa/program-sudoku-generator/


from random import seed, randint
from copy import deepcopy  # Deepcopy solution before changing current (due to nested list)

# Returns false if given 3x3 block contains num
def NumInBox(grid, rowStart, colStart, num):
    for i in range(3):
        for j in range(3):
            if grid[rowStart + i][colStart + j] == num:
                return True
    return False

# Fill a 3x3 matrix (random nums)
def FillBox(grid, row, col):
    for i in range(3):
        for j in range(3):
            while True:
                num = randint(1, 9)
                if not NumInBox(grid, row, col, num): break
            grid[row + i][col + j] = num


def NumInRow(grid, i, num): return num in grid[i]


def NumInCol(grid, j, num):
    for i in range(9):
        if grid[i][j] == num:
            return True
    return False

# Check if it's safe to put num in the cell (i, j)
def CheckIfSafe(grid, i, j, num):
    return (not NumInRow(grid, i, num) and
            not NumInCol(grid, j, num) and
            not NumInBox(grid, i - i % 3, j - j % 3, num))

# Fill the diagonal 3x3 matrices (fast sudoku algo)
def FillDiagonal(grid):
    for i in range(0, 9, 3): FillBox(grid, i, i)

# Fill remaining blocks in the grid
def FillRemaining(grid, i, j):
    if i == 9: return True # End of grid

    if j == 9: return FillRemaining(grid, i + 1, 0) # Next row

    # Skip if cell is already filled
    if grid[i][j] != 0: return FillRemaining(grid, i, j + 1)

    # Try 1-9 in current cell
    for num in range(1, 10):
        if CheckIfSafe(grid, i, j, num):
            grid[i][j] = num
            if FillRemaining(grid, i, j + 1): return True
            grid[i][j] = 0

    return False

def RemoveDigits(grid, numEmpty): # Remove numEmpty digits randomly from grid
    while numEmpty > 0:
        cellId = randint(0, 80)

        # row / col idx
        i = cellId // 9
        j = cellId % 9

        # Remove the digit (if not empty)
        if grid[i][j] != 0:
            grid[i][j] = 0
            numEmpty -= 1

# Generate a Sudoku init/solution set with numEmpty 0's.
def GenerateSudokuSet(numEmpty, RNG=None):
    if numEmpty < 1 or numEmpty > 27:
        print("Invalid numEmpty tiles!")
        return

    # Seed the RNG
    seed(RNG)

    grid = [[0] * 9 for _ in range(9)] # Empty 9x9 grid

    FillDiagonal(grid) # Fill the diagonal 3x3 matrices first
    FillRemaining(grid, 0, 0) # Fill the remaining blocks in the grid

    solution = deepcopy(grid) # Save this solution for later use

    RemoveDigits(grid, numEmpty) # Remove digits to create the puzzle

    return [solution, grid]

#
# Testing
#

numEmpty = 20 # Set the number of empty cells
sudoku = GenerateSudokuSet(numEmpty)

for board in sudoku:
    print("\n")
    for row in board:
        print(" ".join(map(str, row)))
