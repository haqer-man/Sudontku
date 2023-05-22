"""Sudoku Game

This script allows the user to play Sudoku using the CLI.

The file can be imported as a module and contains the following classes:

    * Grid - provides methods to generate, manage, and play Sudoku.

The Grid class contains the following methods:

    * __init__ - creates a Grid object with attributes grid, mask,
    solution, sqrt_N, N, and K
    * fill_values - assigns values to grid, solution, and mask
    * fill_diagonal - assigns values to squares in top left block,
    center block, and bottom right block
    * fill_block - fills a sqrt_N by sqrt_N block with values
    * fill_remaining - recursively fills all empty spaces with values
    * check_position - checks if a given number appears in the row, column,
    and subgrid surrounding a given position
    * check_if_given - checks if a given position is immutable
    * is_solved - returns true if the puzzle is solved
    * num_empty_spaces - returns the number of empty spaces in the grid
    * used_in_row - returns true if the row contains a given number
    * used_in_column - returns true if the column contains a given number
    * used_in_block - returns true if a subgrid contains a given number
    * remove_K_digits - removed K digits from the solution to create the
    playing grid
    * add_num - adds a given number to the grid at a given position
    * __str__ - returns a string representation of the grid
    
The file also contains the following methods:

    * play - plays the game
"""
from random import randint, shuffle
import math

class Grid:
    """The Grid class provides methods to generate, manage,
    and play Sudoku games.
    """
    
    def __init__(self, N:int, K:int):
        """Creates a Grid object with attributes grid,
        mask, solution, sqrt_N, N, and K.
        
        grid stores the 2D array of numbers as the player
        would see.
        
        mask holds a 2D array mask representing which
        values are immutable.
        
        solution holds the 2D array solution.
        
        sqrt_N stores the square root of N to find subgrid
        size.

        Args:
            N (int): a number representing the dimensions
            of the grid
            K (int): a number representing the amount of
            numbers in the grid to begin
        """
        self.N = N
        self.K = K
        
        self.sqrt_N = int(math.sqrt(N))
        self.solution = [[0 for _ in range(N)] for _ in range(N)]
        self.grid = [[0 for _ in range(N)] for _ in range(N)]
        self.mask = [[0 for _ in range(N)] for _ in range(N)]
        
    def fill_values(self)->None:
        """Assigns values to grid, solution, and mask."""
        self.fill_diagonal()
        
        self.fill_remaining(self.sqrt_N - 1, 0)
        
        self.remove_K_digits()
        
    def fill_diagonal(self)->None:
        """Generates values to fill the top left, center,
        and bottom right blocks."""
        for i in range(0, self.N, self.sqrt_N):
            self.fill_block(i, i)
                        
    def fill_block(self, row:int, column:int):
        """Fills a √N x √N block of values.

        Args:
            row (int): topmost row number within block
            column (int): leftmost column number within
            block
        """
        nums = list(range(1,self.N + 1))
        shuffle(nums)
        i = 0
        
        for y in range(self.sqrt_N):
            for x in range(self.sqrt_N):
                self.solution[row+y][column+x] = nums[i]
                i += 1
                
    def fill_remaining(self, x:int, y:int)->bool:
        """Recursively fills squares from left to right
        and top to bottom, making sure no numbers are 
        repeated in a row, column, or block.

        Args:
            x (int): starting x coordinate
            y (int): starting y coordinate

        Returns:
            bool: whether the function has finished
            recurring.
        """
        if y == self.N - 1 and x == self.N:
            return True

        if x == self.N:
            x = 0
            y += 1
            
        if self.solution[y][x] != 0:
            return self.fill_remaining(x + 1, y)
        
        for num in range(1, self.N + 1):
            if self.check_position(x, y, num):
                self.solution[y][x] = num
                if self.fill_remaining(x + 1, y):
                    return True
                self.solution[y][x] = 0
        
        return False
                
    def check_position(self, x:int, y:int, num:int)->bool:
        """Checks if at a position, a given number appears
        only once in that column, row, and subgrid/block.

        Args:
            x (int): x coordinate (1-N)
            y (int): y coordinate (1-N)
            num (int): number to check (1-N)

        Returns:
            bool: true if the number appears only once
            in the row, column, and subgrid/block
        """
        return (not self.used_in_row(y, num)
                and not self.used_in_column(x, num)
                and not self.used_in_block(x, y, num))
        
    def check_if_given(self, x:int, y:int)->bool:
        """Checks if a given position has a starting
        number, and is therefore immutable.

        Args:
            x (int): x coordinate (1-N)
            y (int): y coordinate (1-N)

        Returns:
            bool: true if the given position is
            immutable
        """
        return bool(self.mask[y][x])
    
    def is_solved(self)->bool:
        """Checks if the board is solved.

        Returns:
            bool: true if the board is solved
        """
        return self.grid == self.solution
    
    def num_empty_spaces(self)->int:
        """Gets the number of empty spaces in
        the grid.

        Returns:
            int: the number of spaces with a 0
            on the board
        """
        filled = [
            [1 if space else 0 for space in row]
            for row in self.grid
            ]
        return self.N ** 2 - sum([sum(row) for row in filled])
        
    def used_in_row(self, row:int, num:int)->bool:
        """Checks if a given number is used in a given row.

        Args:
            row (int): row number (1-N)
            num (int): number to check for (1-N)

        Returns:
            bool: true if the number is used in the given row
        """
        return self.solution[row].count(num) != 0
    
    def used_in_column(self, column:int, num:int)->bool:
        """Checks if a given number is used in a given column.

        Args:
            column (int): column number (1-N)
            num (int): number to check for (1-N)

        Returns:
            bool: true if the number is used in the given column
        """
        return [row[column] for row in self.solution].count(num) != 0
        
    def used_in_block(self, x:int, y:int, num:int)->bool:
        """Checks if a given number is used in the subgrid
        surrounding a given point.

        Args:
            x (int): x coordinate (1-N)
            y (int): y coordinate (1-N)
            num (int): number to check for (1-N)

        Returns:
            bool: true if the number is used in the √N x √N
            block surrounding the position (x, y)
        """
        left = x - x % self.sqrt_N
        top = y - y % self.sqrt_N
        
        for curr_x in range(left, left + self.sqrt_N - 1):
            for curr_y in range(top, top + self.sqrt_N - 1):
                if (self.solution[curr_y][curr_x] == num):
                    return True
                
        return False
    
    def remove_K_digits(self)->None:
        """Removes K digits from the grid to create the
        playing grid."""
        used = []
        i = 0
        while i < self.K:
            pos = x, y = randint(0,self.N-1), randint(0,self.N-1)
            if pos not in used:
                used.append(pos)
                self.grid[y][x] = self.solution[y][x]
                self.mask[y][x] = True
                i += 1
                
    def add_num(self, x:int, y:int, num:int)->None:
        """Inserts a number in the playing grid.

        Args:
            x (int): x coordinate to insert number (1-N)
            y (int): y coordinate to insert number (1-N)
            num (int): number to add (1-N)
        """
        self.grid[y][x] = num
                
    #TO-DO: Add compatibility for other size grids
    def __str__(self) -> str:
        """Converts the grid to a string with grid-lines.

        Returns:
            str: a user-readable string with formatting representing the grid
        """
        rows, columns = range(self.N + self.sqrt_N + 1), range(self.N + self.sqrt_N + 1)
        current_y = 0
        output = ''
   
        for row_num in rows:
            if row_num % (self.sqrt_N + 1) == 0:
                output += "+–––––––––+–––––––––+–––––––––+"
                output += '\n' if row_num != (self.N + self.sqrt_N) else ''
                continue
            
            current_x = 0
            
            for column_num in columns:
                if column_num % (self.sqrt_N + 1) == 0:
                    output += "|"
                    output += '\n' if column_num == (self.N + self.sqrt_N) else ''
                    continue
                    
                output += ' ' + str(self.grid[current_y][current_x]) + ' '
                current_x += 1
            current_y += 1
        
        return output
    
def play():
    """Runs the game."""
    N = 9
    K = randint(17, 22)
    grid = Grid(N, K)
    grid.fill_values()
    solved = False
    
    while not solved:
        print(grid)
    
        pos = input("Enter position (\"x, y\"): ").split(', ')
        
        try:        
            y_pos, x_pos = int(pos[1])-1, int(pos[0])-1
        except (IndexError, ValueError):
            print("Invalid position\n\n\n")
            continue
        
        if (not grid.check_if_given(x_pos, y_pos)):
            try:
                num = int(input("Enter number: "))
            except ValueError:
                print("Invalid number\n\n\n")
                continue
            
            if not 0 < num < 9:
                print("Invalid number\n\n\n")
                continue
            
            print('\n\n\n')
            grid.add_num(x_pos, y_pos, num)
            if grid.num_empty_spaces() == 0 and grid.is_solved():
                print(grid)
                solved = True
                print("Congratulations! You won!")
        else:
            print("Position already solved.\n\n\n")

if __name__ == "__main__":
    print("Welcome to Sudontku")
    while True:
        choice = input(
            "Make a selection:\n" +
            "\t1) New game\n" +
            "\t2) Quit\n" +
            "[+] ").strip()
        if choice == '1':
            print()
            play()
        elif choice == '2':
            quit()