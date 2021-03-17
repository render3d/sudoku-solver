# sudoku-solver
A recursive depth first search algorithm which solves sudokus.
An example (Sudoku 5,158 hard) sudoku from The Guardian Newspaper is provided within
  - https://www.theguardian.com/lifeandstyle/2021/mar/12/sudoku-5158-hard

Benchmarks
	- System specifications: Eight-core AMD Ryzen 7 4700U, 8GB RAM
	- 60 out of 60 provided sudokus solved in 288.9 seconds

The solver consists of two primary functions, described as follows:
 - The puzzle is passed to the 'sudoku_solver' function:
	- First the the gid is parsed to check that the input is valid,	i.e. the puzzle in its clean, unsolved state is
		correct and without errors that make it unsolvable. If the input is not valid, the "no solution" grid is 
		returned as the solution.
	- The number of clues given in the initial puzzle is then counted to ensure that there are enough to find a solution
		to the input. This is based on the work of McGuire et al. (https://arxiv.org/abs/1201.0749) who found that
		17 is the minimum number of clues required to give a unique sudoku solution. If there are less than 17 clues,
		the "no solution" grid is returned as the solution.
	- If both of these intial screening tests pass, the unsolved puzzle is copied (so as not to modify the original array)
		and passed to the main 'search' function which finds and returns a solution or the "no solution" grid otherwise,
		as specified.

 - The 'search' function is intended to be a recursive, depth-first search algorithm:
	- First the grid is parsed for any blanks, if there are none, then puzzle is solved. If not, then there are still blanks 
		to be filled and the algorithm proceeds.
	- When there are blanks remaining in the gid, a function is called to return the index of the blank which has the fewest
		possibilities to increase the chances of one of them being the correct one, thus reducing the size of search. Then 
		a possibility is placed in the grid, if the input is is valid, then the search continues, otherwise it backtracks 
		again. If the seach is fruitless then the blank gets reset to zero before backtracking.
	- If the list of minimum possibilities is empty then the function returns False and the algorithm backtracks to the last
		branch.
	- If the list of possibilities is equal to one, the blank is filled with this possibility as it is the only one. As there
		is a possibility that a solution will be reached at this stage, this is checked for after the blank has been filled.
		If this is the csase then the solution is assigned and the search halts. Otherwise, it continues searching.
	- If the list has multiple possibilities then an elementwise, depth-first search operation is performed by creating a copy 
		of the grid for each possibility and then exploring each branch until it reaches a solution or a dead end and 
		backtracking to the next possibility in the list to explore.

 - The remainder of the functions are helpers to the search and solver functions, enabling functionality including, but not limited
		to, parsing or displaying the grid, retrieving blanks, variables, and verifying the conditions/state of the grid. 
		Refer to the pdoc3 HTML documentation and docstrings for complete descriptions of the methods/helper functions.

