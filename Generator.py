
# Generator.py
# Generates a Sudoku initial state and solution.
# Adapted from: https://www.geeksforgeeks.org/dsa/program-sudoku-generator/

import random
# Python program to generate a valid sudoku 
# with k empty cells

# Returns false if given 3x3 block contains num
# Ensure the number is not used in the box
def unUsedInBox(grid, rowStart, colStart, num):
    for i in range(3):
        for j in range(3):
            if grid[rowStart + i][colStart + j] == num:
                return False
    return True

# Fill a 3x3 matrix
# Assign valid random numbers to the 3x3 subgrid
def fillBox(grid, row, col):
    for i in range(3):
        for j in range(3):
            while True:
                # Generate a random number between 1 and 9
                num = random.randint(1, 9)
                if unUsedInBox(grid, row, col, num): break
            grid[row + i][col + j] = num

# Check if it's safe to put num in row i
# Ensure num is not already used in the row
def unUsedInRow(grid, i, num):
    return num not in grid[i]

# Check if it's safe to put num in column j
# Ensure num is not already used in the column
def unUsedInCol(grid, j, num):
    for i in range(9):
        if grid[i][j] == num:
            return False
    return True

# Check if it's safe to put num in the cell (i, j)
# Ensure num is not used in row, column, or box
def checkIfSafe(grid, i, j, num):
    return (unUsedInRow(grid, i, num) and 
            unUsedInCol(grid, j, num) and 
            unUsedInBox(grid, i - i % 3, j - j % 3, num))

# Fill the diagonal 3x3 matrices
# The diagonal blocks are filled to simplify the process
def fillDiagonal(grid):
    for i in range(0, 9, 3):
        
        # Fill each 3x3 subgrid diagonally
        fillBox(grid, i, i)

# Fill remaining blocks in the grid
# Recursively fill the remaining cells with valid numbers
def fillRemaining(grid, i, j):
    
    # If we've reached the end of the grid
    if i == 9:
        return True
    
    # Move to next row when current row is finished
    if j == 9:
        return fillRemaining(grid, i + 1, 0)
    
    # Skip if cell is already filled
    if grid[i][j] != 0:
        return fillRemaining(grid, i, j + 1)
    
    # Try numbers 1-9 in current cell
    for num in range(1, 10):
        if checkIfSafe(grid, i, j, num):
            grid[i][j] = num
            if fillRemaining(grid, i, j + 1):
                return True
            grid[i][j] = 0 
    
    return False

def removeKDigits(grid, k): # Remove K digits randomly from the grid
    while k > 0:
        cellId = random.randint(0, 80)

        # row / col idx
        i = cellId // 9
        j = cellId % 9

        # Remove the digit (if not empty)
        if grid[i][j] != 0:
            grid[i][j] = 0
            k -= 1

# Generate a Sudoku init/solution set with numEmpty 0's.
def sudokuGenerator(numEmpty, seed=0):
    if numEmpty < 1 or numEmpty > 27:
        print("Invalid numEmpty tiles!")
        return

    # Seed the RNG
    if (seed == 0): random.seed() # Default: Random seed
    else: random.seed(seed)
    
    grid = [[0] * 9 for _ in range(9)] # Initialize an empty 9x9 grid

    fillDiagonal(grid) # Fill the diagonal 3x3 matrices
    fillRemaining(grid, 0, 0) # Fill the remaining blocks in the grid

    solution = grid # Save this solution for later use

    removeKDigits(grid, numEmpty) # Remove digits to create the puzzle

    return [solution, grid]


k = 20 # Set the number of empty cells
sudoku = sudokuGenerator(k)

# Print the generated Sudoku puzzle
for row in sudoku: print(" ".join(map(str, row)))
