import numpy as np
from itertools import chain
import time

def displayGrid(sudoku):
    """Prints the sudoku in a more readable format

    Args:
        sudoku (<class 'numpy.ndarray'>): the puzzle in any state

    Returns:
        <class 'NoneType'>: Just prints the grid
    """

    for row in range(len(sudoku)):
        line = ""

        if row == 3 or row == 6:
            print("----------------------")

        for col in range(len(sudoku[row])):
            if col == 3 or col == 6 :
                line += "| "

            if sudoku[row][col] == 0:
                line += " " + " "
            else:
                line += str(int(sudoku[row][col])) + " "

        print(line)

    print("")

    return None

def solved(puzzle):
    """Checks whether a solution to the puzzle has been found by checking if the contents of each cell is unique in its respective row, column or square

    Args:
        puzzle (<class 'numpy.ndarray'>): the puzzle in any state

    Returns:
        <class 'bool'>: False if there are blanks or if any row column or square contains a duplicate number
    """
    solution = True

    if np.any(puzzle == 0):
        solution = False
    else:
        for idx, x in np.ndenumerate(puzzle):
            if not isUnique(getSquare(puzzle, idx)): # check squares have uniques
                solution = False
                return solution
            elif not isUnique(getCol(puzzle, idx)):
                solution = False
                return solution
            elif not isUnique(getRow(puzzle, idx)):
                solution = False
                return solution

    return solution

def getCol(sudoku, idx):
    """Finds the relevant column in which any number resides given the index position of the number, idx, in the sudoku numpy array

    Args:
        sudoku (<class 'numpy.ndarray'>): The puzzle in any state
        idx (<class 'tuple'>): The index postion of the number for which the relevant column must be found

    Returns:
        <class 'numpy.ndarray'>: The column in which the number at index, idx, resides
    """
    col = sudoku[:, idx[1]]

    return col

def getRow(sudoku, idx):
    """Finds the relevant row in which any number resides given the index position of the number, idx, in the sudoku numpy array

    Args:
        sudoku (<class 'numpy.ndarray'>): The puzzle in any state
        idx (<class 'tuple'>): The index postion of the number for which the relevant row must be found

    Returns:
        <class 'numpy.ndarray'>: The row in which the number at index, idx, resides
    """
    row = sudoku[idx[0], :]

    return row

def getSquare(sudoku, idx):
    """Finds the relevant square in which any number resides given the index position of the number, idx, in the sudoku numpy array

    Args:
        sudoku (<class 'numpy.ndarray'>): The puzzle in any state
        idx (<class 'tuple'>): The index postion of the number for which the relevant 3x3 square must be found

    Returns:
        <class 'numpy.ndarray'>: The 3x3 square in which the number at index, idx, resides
    """
    #top row square
    if idx[0] < 3 and idx[1] < 3:
        square = sudoku[0:3, 0:3]

    elif idx[0] < 3 and 3 <= idx[1] < 6:
        square = sudoku[0:3, 3:6]

    elif idx[0] < 3 and 6 <= idx[1] < 9:
        square = sudoku[0:3, 6:9]

    # middle row square
    elif 3 <= idx[0] < 6 and idx[1] < 3:
        square = sudoku[3:6, 0:3]

    elif 3 <= idx[0] < 6 and 3 <= idx[1] < 6:
        square = sudoku[3:6, 3:6]

    elif 3 <= idx[0] < 6 and 6 <= idx[1] < 9:
        square = sudoku[3:6, 6:9]

    # bottom row square
    elif 6 <= idx[0] < 9 and idx[1] < 3:
        square = sudoku[6:9, 0:3]

    elif 6 <= idx[0] < 9 and 3 <= idx[1] < 6:
        square = sudoku[6:9, 3:6]

    elif 6 <= idx[0] < 9 and 6 <= idx[1] < 9:
        square = sudoku[6:9, 6:9]

    return square

def getBlanks(sudoku):
    """Finds the index of each blank tile in an unsolved sudoku and returns them together in a list

    Args:
        sudoku (<class 'numpy.ndarray'>): The puzzle in its unsolved state

    Returns:
        <class 'list'>: The list of indices at which there is a blank space in the puzzle, i.e. the list of blanks to be filled by the search algorithm
    """
    row, col = np.where(sudoku == 0)

    blanks = []
    y = 0
    for x in row:
        blanks.append((x,col[y]))
        y += 1

    return blanks

def getVariables(sudoku, blank):
    """Finds a list of valid possibilities of a given empty cell in the unsolved sudoku

    Args:
        sudoku (<class 'numpy.ndarray'>): The puzzle in its unsolved state
        blank (<class 'tuple'>): The index of the blank in the puzzle

    Returns:
        <class 'list'>: The list of possibilities for a given blank after variables have been eliminated
    """
    variables = [x for x in range(1,10)]
    possibilities = []

    for v in variables:
        if checkRow(sudoku, blank, v): # search rows
            pass
        elif checkCol(sudoku, blank, v): # search columns
            pass
        elif checkSquare(sudoku, blank, v): # search boxes
            pass
        else:
            possibilities.append(v)

    return possibilities

def checkRow(sudoku, idx, num):
    """Checks whether a number is already present in a 1x9 row of the sudoku puzzle

    Args:
        sudoku (<class 'numpy.ndarray'>): The puzzle in its unsolved state
        idx (<class 'tuple'>): The index of the blank which must be filled
        num ('int'): The variable to check if present or not

    Returns:
        <class 'bool'>: True if num present in relevant 1x9 row, False otherwise
    """
    present = False

    for col in range(len(sudoku)):
        if sudoku[idx[0], col] == num:
            present = True

    return present

def checkCol(sudoku, idx, num):
    """Checks whether a number is already present in a 1x9 column of the sudoku puzzle

    Args:
        sudoku (<class 'numpy.ndarray'>): The puzzle in its unsolved state
        idx (<class 'tuple'>): The index of the blank which must be filled
        num ('int'): The variable to check if present or not

    Returns:
        <class 'bool'>: True if num present in relevant 1x9 column, False otherwise
    """
    present = False

    for row in range(len(sudoku)):
        if sudoku[row, idx[1]] == num:
            present = True

    return present

def checkSquare(sudoku, idx, num):
    """Checks whether a number is already present in a 3x3 square of the sudoku puzzle

    Args:
        sudoku (<class 'numpy.ndarray'>): The puzzle in its unsolved state
        idx (<class 'tuple'>): The index of the blank which must be filled
        num ('int'): The variable to check if present or not

    Returns:
        <class 'bool'>: True if num present in relevant 3x3 square, False otherwise
    """
    present = False
    square = list(chain.from_iterable(getSquare(sudoku, idx).tolist()))
    # square = getSquare(sudoku, idx)[getSquare(sudoku, idx) != 0]
    square.sort()

    if num in square:
        present = True

    return present

def enoughClues(sudoku):
    """Uses principle that 17 is the minimum number of clues required to give a unique sudoku solution, as proved by McGuire et al. https://arxiv.org/abs/1201.0749

    Args:
        puzzle (<class 'numpy.ndarray'>): Sudoku puzzle in its unsolved state

    Returns:
        <class 'bool'>: True if there are enough clues to solve the puzzle, False otherwise
    """
    clues = (len(sudoku)**2) - np.count_nonzero(sudoku == 0)

    if clues > 16:
        solvable = True
    else:
        solvable = False

    return solvable

def isUnique(arr):
    """Determines whether numbers in input array (i.e. sudoku row, column, square) are unique or not

    Args:
        arr (<class 'numpy.ndarray'>): sudoku row, column or square

    Returns:
        <class 'bool'>: True if there are no duplicates in input array, False otherwise
    """
    unique = True

    uniq = arr[arr != 0]
    discard, freq = np.unique(uniq, return_counts = True)

    try:
        if max(freq) > 1:
            unique = False
    except:
        # print("No clues")
        pass

    return unique

def validInput(puzzle):
    """Function which checks whether the input puzzle has any errors.
    Error types:\\
        - Two identical numbers in the same row
        - Two identical numbers in the same column
        - Two identical numbers in the same 3x3 square
        - For a given blank cell, there are no valid possibilities because in the same row and column of that cell\\
            there already exists the numbers 1-9. As such there are no valid possibilities and the puzzle is sunsolvable.

    Args:
        puzzle (<class 'numpy.ndarray'>): A puzzle in its unsolved state

    Returns:
        <class 'bool'>: True if no puzzle is valid, False otherwise
    """
    valid = True

    for row in range(len(puzzle)): # checking rows for duplication errors
        if not isUnique(puzzle[row,:]):
            valid = False
            return valid

    for col in range(len(puzzle)): # checking cols for duplication errors
        if not isUnique(puzzle[:,col]):
            valid = False
            return valid

    for row in [0,3,6]: # checking squares for duplication errors
        for col in [0,3,6]:
            if not isUnique(getSquare(puzzle, [row,col])):
                valid = False
                return valid

    return valid

def getOptimumBlank(sudoku):
    """Finds the empty cell in the sudoku grid with the minimum number of possibilities to increase the chances of finding the correct one.

    Args:
        sudoku (<class 'numpy.ndarray'>): The puzzle in any state

    Returns:
        idx (<class 'tuple'>): The index of the blank with the minimum number of possibilities
        varlist (<class 'list'>): The list of possibilities
    """

    blanks = getBlanks(sudoku)

    possibilities = {}
    for blank in blanks:
        variables = getVariables(sudoku, blank)
        possibilities.update({blank: variables})

    length, idx, varlist = min((len(possibilities[blank]), blank, possibilities[blank]) for blank in possibilities)

    return idx, varlist

def search(sudoku):
    """The recursive constrained depth first search algorithm with backtracking to solve input sudoku puzzle

    Args:
        sudoku (<class 'numpy.ndarray'>): The puzzle in any state

    Returns:
        <class 'bool'>: True if valid, False otherwise
    """

    try:
        blank = getBlanks(sudoku)[0]
    except IndexError:
        blank = None

    if blank is None:
        return True

    idx, varlist = getOptimumBlank(sudoku)

    # print(idx, varlist)
    if len(varlist) == 0:
        pass
    else:
        if len(varlist) == 1:
            # print("For", idx, "there is only one possibility, inserting:", varlist[0])
            sudoku[idx] = varlist[0]
            # displayGrid(sudoku)

            if solved(sudoku):
                global solution # a bit hacky but was the only way I could find to return/retrieve the solution
                solution = sudoku
                return True
            else:
                if validInput(sudoku):
                    if search(sudoku):
                        return True

                    sudoku[idx] = 0
        else:
            for var in varlist:
                # print("Attempting with a", var, "in blank", idx)
                branch = np.copy(sudoku)
                branch[idx] = var
                sudoku = branch
                # displayGrid(branch)

                if validInput(branch):
                    if search(branch):
                        return True

                    sudoku[idx] = 0

    return False

def sudoku_solver(puzzle):
    """Checks the input is valid and solvable prior to initiating the search algorithm

    Args:
        sudoku (<class 'numpy.ndarray'>): The puzzle in an unsolved state

    Returns:
        <class 'numpy.ndarray'>: The solution to the puzzle i.e. all blanks correctly filled
    """

    if not validInput(puzzle): # checks input valid
        print("Input not valid.")
        solved_puzzle = np.ones((9, 9), dtype = np.int8)*-1
    elif not enoughClues(puzzle): # checks for enough clues
        print("Input not solvable.")
        solved_puzzle = np.ones((9, 9), dtype = np.int8)*-1
    else:
        print("Input valid and solvable, solving...")
        ### YOUR CODE HERE
        global sudoku
        sudoku = np.copy(puzzle)
        if search(sudoku):
            solved_puzzle = solution
        else:
            solved_puzzle = np.ones((9, 9), dtype = np.int8)*-1

    return solved_puzzle

### Example Input

sudoku = np.array([[0,0,0,0,0,0,0,0,2],
                    [9,7,5,0,0,0,4,0,0],
                    [0,0,3,0,0,6,7,5,0],
                    [0,1,0,4,2,0,0,0,7],
                    [0,0,0,0,0,0,0,0,0],
                    [2,0,0,0,5,9,0,4,0],
                    [0,5,7,9,0,0,1,0,0],
                    [0,0,1,0,0,0,5,7,6],
                    [6,0,0,0,0,0,0,0,0]])

print("Input puzzle: Sudoku 5,158 hard from The Guardian")
# https://www.theguardian.com/lifeandstyle/2021/mar/12/sudoku-5158-hard
displayGrid(sudoku)

start = time.time()
solution = sudoku_solver(sudoku)
end = time.time()

total = end - start

print("Solution found in", total, "seconds:")
displayGrid(solution)
