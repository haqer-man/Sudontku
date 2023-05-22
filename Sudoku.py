"""Sudoku Game

This script allows the user to play Sudoku, or run a backtracking algorithm to autosolve.\
It is assumed that the user's screen has a resolution of 650x720 or higher.

The script requires that `pygame` be installed within the Python environment you are running\
it in.

The file can be imported as a module and contains the following functions:

    * clear_grid - clears the play area for a new game
    * write_to_grid - writes a number to a space in the grid
    * write_note_to_grid - writes a note to a space in the grid
    * """  # TODO: finish Docstring header
# Import Modules
from random import randint, shuffle
import math
import pygame as pg
from time import sleep

if not pg.font:
    print("Warning, fonts disabled")

# Start pygame
pg.init()

# Define constants
WHITE = 255, 255, 255
BLACK = 10, 10, 10
GRAY = 209, 206, 197
DIM_GRAY = 171, 171, 164
DARKENED_GRAY = 69, 67, 66
LIGHT_BLUE = 69, 218, 255
DIM_LIGHT_BLUE = 64, 203, 237
DARKENED_LIGHT_BLUE = 60, 188, 219
LIGHT_PINK = 237, 142, 176
DIM_LIGHT_PINK = 219, 129, 161
DARKENED_LIGHT_PINK = 201, 105, 139

SIZE = WIDTH, HEIGHT = 650, 720
X_PADDING, Y_PADDING = 15, 5
GRID_DIMENSION = 4 * WIDTH / 5
BOX_SIZE = GRID_DIMENSION / 9

MAIN_FONT_PATH = pg.font.match_font("pingfang")
MAIN_FONT_SIZE = 36
MAIN_FONT = pg.font.Font(MAIN_FONT_PATH, MAIN_FONT_SIZE)
NUM_FONT_PATH = pg.font.match_font("americantypewriter")
NUM_FONT_SIZE = 48
NUM_FONT = pg.font.Font(NUM_FONT_PATH, NUM_FONT_SIZE)
NOTE_FONT_PATH = pg.font.match_font("farah")
NOTE_FONT = pg.font.Font(NOTE_FONT_PATH, 20)
BUTTON_FONT_PATH = pg.font.match_font("courier")
BUTTON_FONT_SIZE = 36
BUTTON_FONT = pg.font.Font(BUTTON_FONT_PATH, BUTTON_FONT_SIZE)
WIN_FONT_PATH = pg.font.match_font('menlo', True)


class Grid:
    """A class used to represent a Sudoku grid
    
    ...
    
        Attributes
        ----------
    focused : tuple[int, int]
        the coordinate of the currently focused cell
    grid : list[list[int]]
        the grid to be solved
    K : int
        the number of starting numbers to be given to the player
    mask : list[list[int]]
        masked list representing whether each cell is immutable
    N : int
        the number of cells per row and column
    notes : list[list[list[int]]]
        3-dimensional list, holding a masked list of notes for each
        cell
    selected : tuple[int, int]
        the coordinate of the currently selected cell
    solution : list[list[int]]
        the fully solved grid
    sqrt_N : int
        the square root of N rounded down to the nearest integer
    
        Methods
        -------
    check_if_given(x: int, y: int) -> bool
        checks if a given position is immutable
    check_position(x: int, y: int, num: int) -> bool
        checks if a number already appears in a row, column, and
        subgrid
    clear_all_notes() -> None
        erases all notes
    clear_note(x: int, y: int, num: int) -> None
        erases a note from a cell
    clear_notes_in_cell(x: int, y: int) -> None
        erases all notes in a cell
    clear_nums() -> None
        resets the grid
    fill_block(row: int, column: int) -> None
        fills the values in the subgrid at the given row and column
    fill_diagonal() -> None
        fills the top left, center, and bottom right blocks with
        values
    fill_remaining(x: int, y: int) -> bool
        recursively fills the remaining cells in the grid
    fill_values() -> None
        assigns values in the grid, solution, and mask
    get_focused_cell() -> tuple[int, int]
        returns the coordinate of the currently focused cell
    get_grid() -> list[list[int]]
        returns the grid as a 2D list of integers
    get_N() -> int
        returns the value of N
    get_notes_from_cell(x: int, y: int) -> list[int]
        returns the masked list of notes in a cell
    get_selected_cell() -> tuple[int, int]
        returns the position of the currently selected cell
    get_solution() -> list[list[int]]
        returns the solution as a 2D list of integers
    get_sqrt_N() -> int
        returns the square root of N rounded down to the nearest
        integer
    is_solved() -> bool
        checks if the grid is solved
    num_empty_spaces() -> int
        gets the number of empty spaces in the grid
    remove_K_digits() -> None
        clears K cells in the grid
    remove_num(x: int, y: int) -> None
        clears the cell at a given position
    set_focused_cell(focused: tuple[int, int]) -> None
        sets the focused cell to the cell at the given position
    set_selected_cell(selected: tuple[int, int]) -> None
        sets the selected cell to the cell at the given position
    used_in_block(x: int, y: int, num: int) -> bool
        checks if a number already appears in a subgrid
    used_in_column(column: int, num: int) -> bool
        checks if a number already appears in a given column
    used_in_row(row: int, num: int) -> bool
        checks if a number already appears in a given row
    write_note(x: int, y: int, num: int) -> None
        writes a note to a cell
    write_num(num: int, x: int, y: int) -> None
        adds a number to the grid
    """

    def __init__(self, N: int, K: int):
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
            numbers the user will start with
        """
        self.selected = (-1, -1)
        self.focused = (-1, -1)
        self.N = N
        self.K = K
        self.sqrt_N = int(math.sqrt(N))
        self.solution = [[0 for _ in range(N)] for _ in range(N)]
        self.grid = [[0 for _ in range(N)] for _ in range(N)]
        self.mask = [[0 for _ in range(N)] for _ in range(N)]
        self.notes = [
            [
                [0 for _ in range(N)]
                for _ in range(N)
            ] for _ in range(N)
        ]

    def fill_values(self) -> None:
        """Assigns values to solution, mask, and grid, where solution
        is the solution to the puzzle, mask is an array mask representing
        which values are immutable, and grid is the playing grid."""
        
        self.fill_diagonal()

        self.fill_remaining(self.sqrt_N - 1, 0)

        self.remove_K_digits()

    def fill_diagonal(self) -> None:
        """Generates values to fill the top left, center,
        and bottom right subgrids."""
        
        for i in range(0, self.N, self.sqrt_N):
            self.fill_block(i, i)

    def fill_block(self, row: int, column: int) -> None:
        """Fills a √N x √N block of values.

        Args:
            row (int): topmost row number within block
            column (int): leftmost column number within
            block
        """
        
        nums = list(range(1, self.N + 1))
        shuffle(nums)
        i = 0

        for y in range(self.sqrt_N):
            for x in range(self.sqrt_N):
                self.solution[row+y][column+x] = nums[i]
                i += 1

    def fill_remaining(self, x: int, y: int) -> bool:
        """Recursively fills squares from left to right
        and top to bottom, making sure no numbers are 
        repeated in a row, column, or block.

        Args:
            x (int): starting x coordinate
            y (int): starting y coordinate

        Returns:
            bool: True if the base condition has been
            reached, False otherwise
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

    def check_position(self, x: int, y: int, num: int) -> bool:
        """Checks if at a position, a given number appears
        only once in that column, row, and subgrid/block.

        Args:
            x (int): x coordinate
            y (int): y coordinate
            num (int): number to check

        Returns:
            bool: true if the number appears only once
            in the row, column, and subgrid/block
        """
        
        return (not self.used_in_row(y, num)
                and not self.used_in_column(x, num)
                and not self.used_in_block(x, y, num))

    def used_in_row(self, row: int, num: int) -> bool:
        """Checks if a given number is used in a given row.

        Args:
            row (int): row number
            num (int): number to check for

        Returns:
            bool: true if the number is used in the given row
        """
        
        return self.solution[row].count(num) != 0

    def used_in_column(self, column: int, num: int) -> bool:
        """Checks if a given number is used in a given column.

        Args:
            column (int): column number
            num (int): number to check for

        Returns:
            bool: true if the number is used in the given column
        """
        
        return [row[column] for row in self.solution].count(num) != 0

    def used_in_block(self, x: int, y: int, num: int) -> bool:
        """Checks if a given number is used in the subgrid
        surrounding a given point.

        Args:
            x (int): x coordinate
            y (int): y coordinate
            num (int): number to check for

        Returns:
            bool: true if the number is used in the √N x √N
            block surrounding the position (x, y)
        """
        
        left = x - x % self.sqrt_N
        top = y - y % self.sqrt_N

        for curr_x in range(left, left + self.sqrt_N):
            for curr_y in range(top, top + self.sqrt_N):
                if (self.solution[curr_y][curr_x] == num):
                    return True

        return False
    
    def check_if_given(self, x: int, y: int) -> bool:
        """Checks if a given position has a starting
        number, and is therefore immutable.

        Args:
            x (int): x coordinate
            y (int): y coordinate

        Returns:
            bool: true if the given position is
            immutable
        """
        
        return bool(self.mask[y][x])

    def is_solved(self) -> bool:
        """Checks if the board is solved.

        Returns:
            bool: true if the board is solved
        """

        return self.grid == self.solution

    def num_empty_spaces(self) -> int:
        """Gets the number of empty cells in the grid

        Returns:
            int: the number of empty cells in the grid
        """
        
        filled = [
            [1 if space else 0 for space in row]
            for row in self.grid
        ]
        return self.N ** 2 - sum([sum(row) for row in filled])

    def remove_K_digits(self) -> None:
        """Removes K digits from the grid to create the
        playing grid."""
        
        used = []
        i = 0
        while i < self.K:
            pos = x, y = randint(0, self.N-1), randint(0, self.N-1)
            if pos not in used:
                used.append(pos)
                self.grid[y][x] = self.solution[y][x]
                self.mask[y][x] = True
                i += 1

    def write_num(self, num: int, x: int, y: int) -> None:
        """Inserts a number in the playing grid.

        Args:
            x (int): x coordinate
            y (int): y coordinate
            num (int): number
        """
        
        self.grid[y][x] = num

    def remove_num(self, x: int, y: int) -> None:
        """Removes a number from the playing grid.

        Args:
            x (int): x coordinate to remove number
            y (int): y coordinate to remove number
        """
        
        self.grid[y][x] = 0

    def clear_nums(self) -> None:
        """Clears all non-given numbers from the grid."""
        for i in range(self.N):
            for j in range(self.N):
                if not self.check_if_given(i, j):
                    self.grid[j][i] = 0

    def write_note(self, x: int, y: int, num: int) -> None:
        """Writes a note to a cell on the grid.

        Args:
            num (int): The number to write
            x (int): x coordinate
            y (int): y coordinate
        """
        
        self.notes[y][x][num - 1] = 1

    def clear_note(self, x: int, y: int, num: int) -> None:
        """Deletes a note from a cell on the grid.

        Args:
            x (int): x coordinate
            y (int): y coordinate
            num (int): number
        """
        
        self.notes[y][x][num - 1] = 0

    def clear_notes_in_cell(self, x: int, y: int) -> None:
        """Deletes all notes from a cell.

        Args:
            x (int): x coordinate
            y (int): y coordinate
        """
        
        self.notes[y][x] = [0 for _ in range(self.N)]

    def clear_all_notes(self) -> None:
        """Clears all notes from all cells."""
        
        for y in range(self.N):
            for x in range(self.N):
                self.clear_notes_in_cell(x, y)

    def get_notes_from_cell(self, x: int, y: int) -> list[int]:
        """Returns a mask representing the notes in a cell.

        Args:
            x (int): x coordinate
            y (int): y coordinate

        Returns:
            list[int]: mask representing the number notes in the
            cell (i.e. [1, 1, 0, 0, 1, 1, 0, 0, 0] would mean the
            cell has notes 1, 2, 5, and 6)
        """
        
        return self.notes[y][x]

    def get_grid(self) -> list[list[int]]:
        """Gets the grid as a 2D list of integers.

        Returns:
            tuple[int, int]: 2D list of the integers in the grid in
            row-major order.
        """
        
        return self.grid

    def get_N(self) -> int:
        """Gets the value of N.

        Returns:
            int: N, the number of cells per row
        """
        
        return self.N

    def get_sqrt_N(self) -> int:
        """Gets the int value of the square root of N.

        Returns:
            int: square root of N
        """
        
        return self.sqrt_N

    def get_selected_cell(self) -> tuple[int, int]:
        """Gets the coordinate of the selected cell.

        Returns:
            tuple[int, int]: selected coordinate (x, y)
        """
        
        return self.selected

    def set_selected_cell(self, selected: tuple[int, int]) -> None:
        """Sets the selected cell to a specified position (x, y).

        Args:
            selected (tuple[int, int]): coordinate (x, y)
        """
        
        self.selected = selected

    def get_focused_cell(self) -> tuple[int, int]:
        """Gets the coordinate of the focused cell.

        Returns:
            tuple[int, int]: focused coordinate (x, y)
        """
        
        return self.focused

    def set_focused_cell(self, focused: tuple[int, int]) -> None:
        """Sets the focused cell to a specified position (x, y).

        Args:
            focused (tuple[int, int]): coordinate (x, y)
        """
        
        self.focused = focused

    def get_solution(self) -> list[list[int]]:
        """Gets the solution to the puzzle.

        Returns:
            list[list[int]]: 2D array of integers in the solution
            in row-major order
        """
        
        return self.solution

    # TODO: Add compatibility for other size grids


class UI(object):
    # TODO: write docstring

    def draw_menu() -> None:
        """Draws the menu, consisting of the background Surface."""
        
        global background
        background = pg.Surface(SIZE).convert_alpha()
        background.fill((*WHITE, 255))

        UI.draw_background()
        UI.generate_blank_grid()
        pg.display.flip()

    def draw_background() -> None:
        """Draws the background, consisting of the header, play
        button, and exit button."""
        
        UI.draw_header()
        UI.draw_menu_buttons()

        screen.blit(background, (0, 0))

    def draw_header() -> None:
        """Draws the header."""
        
        global header_rect_bottom

        font = pg.font.Font(MAIN_FONT_PATH, MAIN_FONT_SIZE)
        #text = font.render("Play Sudoku or Let the Computer Play", True, BLACK)
        text = font.render("Play Sudoku", True, BLACK)
        y = 10
        textpos = text.get_rect(centerx=WIDTH/2, y=y)
        header_rect_bottom = textpos.height + y
        background.blit(text, textpos)

    def generate_blank_grid() -> None:
        """Creates the global Surface variable blank_grid,
        which has the grid lines drawn in it."""
        
        global blank_grid
        blank_grid = pg.Surface(
            (GRID_DIMENSION+3, GRID_DIMENSION+3)).convert_alpha()
        blank_grid.fill((*WHITE, 0))

        for i in range(10):
            line_width = 3 if i % 3 == 0 or i == 0 else 1

            pg.draw.line(  # draw vertical lines
                blank_grid,
                (*BLACK, 255),
                (i * BOX_SIZE + 1, 0),
                (i * BOX_SIZE + 1, 9 * BOX_SIZE + 2),
                line_width
            )
            pg.draw.line(  # draw horizontal lines
                blank_grid,
                (*BLACK, 255),
                (0, i * BOX_SIZE + 1),
                (9 * BOX_SIZE + 2, i * BOX_SIZE + 1),
                line_width
            )

    def generate_grid_rects() -> None:
        """Creates global list of Rectangle objects grid_rects,
        used for coloring cells."""
        
        global grid_rects

        font = pg.font.Font(NUM_FONT_PATH, NUM_FONT_SIZE)
        grid_pos = UI.get_grid_pos()
        # TODO: find scalable way to do this
        left, top = grid_pos[0], grid_pos[1] - 12
        grid_rects = []
        for row in range(grid.get_N()):
            row_rects = []
            if row == 3:
                top += 1
            for col in range(grid.get_N()):
                row_rects.append(
                    pg.Rect(
                        left + 1 + col * BOX_SIZE,
                        top + row - font.get_ascent() + (row + 1) * (BOX_SIZE - 1),
                        BOX_SIZE + 1,
                        BOX_SIZE + 1
                    )
                )
            grid_rects.append(row_rects)

    def draw_blank_grid() -> None:
        """Draws blank_grid Surface to screen."""
        
        screen.blit(blank_grid, UI.get_grid_pos())

    def draw_grid() -> None:
        """Draws all numbers into the grid."""
        
        pg.draw.rect(screen, WHITE, blank_grid.get_rect(
            topleft=UI.get_grid_pos()))
        UI.draw_blank_grid()

        _grid = grid.get_grid()

        for y in range(grid.get_N()):
            for x in range(grid.get_N()):
                if _grid[y][x] == 0:
                    continue

                if (grid.check_if_given(x, y)):
                    NUM_FONT.set_bold(True)

                text = NUM_FONT.render(str(_grid[y][x]), True, BLACK)
                cell_rect = grid_rects[y][x]
                textpos = text.get_rect(
                    centerx=cell_rect.centerx,
                    centery=cell_rect.centery
                )
                screen.blit(text, textpos)
                NUM_FONT.set_bold(False)

        pg.display.update(blank_grid.get_rect(topleft=UI.get_grid_pos()))

    def draw_num(num: int) -> None:
        """Draws a number to the selected cell.

        Args:
            num (int): number to draw
        """
        
        col, row = grid.get_selected_cell()
        if (col, row) == (-1, -1):
            return

        cell_rect = grid_rects[row][col]

        UI.delete_num()

        grid.write_num(int(num), col, row)

        num_text = NUM_FONT.render(str(num), True, BLACK)
        num_pos = num_text.get_rect(
            centerx=cell_rect.centerx,
            centery=cell_rect.centery
        )
        screen.blit(num_text, num_pos)
        UI.draw_blank_grid()

        pg.display.update(cell_rect)

        if grid.is_solved():
            UI.win()

    def draw_num_to_cell(num: int, col: int, row: int) -> None:
        """Draws a number to the cell at a given coordinate.

        Args:
            num (int): number
            col (int): x coordinate
            row (int): y coordinate
        """
        
        # TODO: remove num from notes in row, column, and subgrid when new num is played
        if num == 0:
            UI.draw_notes((col, row))
            UI.draw_blank_grid()
            pg.display.flip()
            return
        else:
            grid.clear_notes_in_cell(col, row)

        num_text: pg.Surface = NUM_FONT.render(str(num), True, BLACK)

        cell_rect: pg.Rect = grid_rects[row][col]
        num_pos: pg.Rect = num_text.get_rect(
            centerx=cell_rect.centerx,
            centery=cell_rect.centery
        )
        screen.blit(num_text, num_pos)

    def delete_num() -> None:
        """Clears a cell."""
        
        col, row = grid.get_selected_cell()
        if (col, row) == (-1, -1):
            return

        grid.remove_num(col, row)
        grid.clear_notes_in_cell(col, row)

        pg.draw.rect(screen, DIM_GRAY, grid_rects[row][col])
        UI.draw_blank_grid()
        pg.display.update(grid_rects[row][col])

    # TODO: add buffer for undo

    def clear() -> None:
        """Clears all mutable cells."""
        
        grid.clear_nums()
        grid.clear_all_notes()
        grid.set_selected_cell((-1, -1))
        UI.draw_grid()
        UI.focus_cell()
        pg.display.update(blank_grid.get_rect(topleft=UI.get_grid_pos()))

    def toggle_note(num: int, pos: tuple[int, int] = None) -> None:
        """Toggles the note for a given number in a cell at a given position.

        Args:
            num (int): number to toggle
            pos (tuple[int, int], optional): coordinate (x, y).
            Defaults to None.
        """
        
        col, row = pos if pos else grid.get_selected_cell()
        if (col, row) == (-1, -1):
            return

        if grid.get_grid()[row][col] != 0:
            return

        if grid.get_notes_from_cell(col, row)[num - 1] == 1:
            grid.clear_note(col, row, num)
            pg.draw.rect(screen, DIM_GRAY, grid_rects[row][col])
            UI.draw_notes()
            UI.draw_blank_grid()
            pg.display.update(grid_rects[row][col])
            return

        grid.write_note(col, row, num)
        UI.draw_note(num)
        UI.draw_blank_grid()
        pg.display.update(grid_rects[row][col])

    def draw_note(num: int, pos: tuple[int, int] = None) -> None:
        """Draws a note for a given number in a cell at a given position.

        Args:
            num (int): number to draw
            pos (tuple[int, int], optional): coordinate (x, y).
            Defaults to None.
        """
        
        col, row = pos if pos else grid.get_selected_cell()

        if grid.get_grid()[row][col] == 1:
            return

        note_text = NOTE_FONT.render(str(num), True, BLACK)

        cell_rect: pg.Rect = grid_rects[row][col]

        left, top = cell_rect.topleft
        textpos = note_text.get_rect(
            topleft=(
                left + 5 + int((num - 1) % 3) * (BOX_SIZE / 3),
                top + int((num - 1) / 3) * (BOX_SIZE / 3)
            )
        )

        screen.blit(note_text, textpos)

    def draw_notes(pos: tuple[int, int] = None) -> None:
        """Draws all notes in a given cell.

        Args:
            pos (tuple[int, int], optional): coordinate (x, y).
            Defaults to selected cell.
        """
        
        x, y = pos if pos else grid.get_selected_cell()
        notes = grid.get_notes_from_cell(x, y)

        for i, n in enumerate(notes):
            if n != 0:
                UI.draw_note(i + 1, (x, y))

    def clear_notes() -> None:
        """Removes all notes from selected cell."""
        
        x, y = grid.get_selected_cell()

        if (x, y) == (-1, -1):
            return

        grid.clear_notes_in_cell(x, y)
        pg.draw.rect(screen, DIM_GRAY, grid_rects[y][x])
        UI.draw_blank_grid()
        pg.display.update(grid_rects[y][x])

    def focus_cell() -> None:
        """Focuses the cell that the mouse is currently on."""
        
        if not UI.mouse_in_grid():
            UI.unfocus_cell()
            return

        x, y = pos = UI.get_pos_from_mouse()

        if grid.check_if_given(x, y):
            UI.unfocus_cell()
            return

        prev_x, prev_y = prev_pos = grid.get_focused_cell()
        if prev_pos == (x, y):
            return

        _grid = grid.get_grid()

        if prev_pos != grid.get_selected_cell() and prev_pos != (-1, -1):
            UI.unfocus_cell((prev_x, prev_y))

        if pos != grid.get_selected_cell() and pos != prev_pos:
            pg.draw.rect(screen, GRAY, grid_rects[y][x])
            grid.set_focused_cell((x, y))
            UI.draw_num_to_cell(_grid[y][x], x, y)

        UI.draw_blank_grid()
        pg.display.update(grid_rects[y][x])
        pg.display.update(grid_rects[prev_y][prev_x])

    def unfocus_cell(pos: tuple[int, int] = None) -> None:
        """Unfocuses a cell.

        Args:
            pos (tuple[int, int], optional): coordinate (x, y).
            Defaults to currently focused cell.
        """
        
        x, y = pos if pos else grid.get_focused_cell()
        if (x, y) == (-1, -1):
            return

        pg.draw.rect(screen, WHITE, grid_rects[y][x])
        UI.draw_num_to_cell(grid.get_grid()[y][x], x, y)
        grid.set_focused_cell((-1, -1))

    def select_cell(pos: tuple[int, int] = None) -> None:
        """Selects a cell.

        Args:
            pos (tuple[int, int], optional): coordinate (x, y).
            Defaults to the cell the mouse is on.
        """
        
        # TODO: highlight all of the same number in the grid
        x, y = pos if pos else UI.get_pos_from_mouse()
        if grid.check_if_given(x, y):
            return

        prev_x, prev_y = grid.get_selected_cell()
        if prev_x == x and prev_y == y:
            return

        UI.unselect_cell()
        grid.set_focused_cell((-1, -1))

        _grid = grid.get_grid()

        pg.draw.rect(screen, DIM_GRAY, grid_rects[y][x])
        grid.set_selected_cell((x, y))

        UI.draw_num_to_cell(_grid[y][x], x, y)

        UI.draw_blank_grid()
        pg.display.update(grid_rects[y][x])
        pg.display.update(grid_rects[prev_y][prev_x])

    def move_left() -> None:
        """Selects the cell one space to the left. If the cell
        to the left is immutable, moves to the next cell to the
        left that is mutable."""
        
        pass

    def move_right() -> None:
        """Selects the cell one space to the right. If the cell
        to the right is immutable, moves to the next cell to the
        right that is mutable."""
        
        pass

    def move_up() -> None:
        """Selects the cell one space up. If the cell is immutable
        moves up until a mutable cell is selected."""
        
        pass

    def move_down() -> None:
        """Selects the cell one space down. If the cell is immutable,
        moves down until a mutable cell is selected."""
        
        pass

    def unselect_cell() -> None:
        """Unselects the currently selected cell."""
        
        x, y = grid.get_selected_cell()
        if (x, y) == (-1, -1):
            return

        pg.draw.rect(screen, WHITE, grid_rects[y][x])
        UI.draw_num_to_cell(grid.get_grid()[y][x], x, y)

    def mouse_in_grid() -> bool:
        """Checks whether the mouse is within the grid.

        Returns:
            bool: True if the mouse is within the edges of
            the grid, False otherwise.
        """
        
        left, top = UI.get_grid_pos()
        return blank_grid.get_rect(
            topleft=(left+3, top+3),
            width=blank_grid.get_width() - 6,
            height=blank_grid.get_height() - 6
        ).contains((*pg.mouse.get_pos(), 0, 0))

    def get_pos_from_mouse() -> tuple[int, int]:
        """Returns the grid coordinate based on the mouse
        position.

        Returns:
            tuple[int, int]: coordinate (x, y)
        """
        
        top, left = UI.get_grid_pos()[::-1]
        mouse_x, mouse_y = pg.mouse.get_pos()

        x = int((mouse_x - left) / BOX_SIZE)
        y = int((mouse_y - top) / (BOX_SIZE + .5))

        if x < 0:
            x = 0
        elif x > 8:
            x = 8

        if y < 0:
            y = 0
        elif y > 8:
            y = 8

        return x, y

    def get_grid_pos() -> tuple[int | float, int | float]:
        """Returns the topleft coordinate of the grid
        on the screen."""
        
        x = (WIDTH - blank_grid.get_rect().width) / 2
        y = header_rect_bottom + \
            ((play_button_rect.top - header_rect_bottom -
             blank_grid.get_rect().height) / 2)
        return (x, y)

    def draw_menu_buttons() -> None:
        """Draws the play and exit buttons."""
        
        UI.draw_exit_button()
        UI.draw_play_button()

    def draw_game_buttons() -> None:
        """Draws the clear and note buttons."""
        
        UI.draw_clear_button()
        UI.draw_note_button()

    def draw_button_rect(rect: pg.Rect, color: tuple[int, int, int]) -> None:
        """Draws a given rectangle in a given color. Used to
        more easily change the color of buttons.

        Args:
            rect (pg.Rect): rectangle object for button
            color (tuple[int, int, int]): RGB color
        """
        
        pg.draw.rect(screen, color, rect, 0, 3)

    def draw_play_button() -> None:
        """Draws the play button."""
        
        text, textpos = UI.generate_play_text()

        UI.draw_button_rect(play_button_rect, LIGHT_BLUE)
        screen.blit(text, textpos)
        pg.display.update(play_button_rect)

    def generate_play_text() -> tuple[pg.Surface, pg.Rect]:
        """Creates the text Surface and textpos Rect
        objects for the play button.

        Returns:
            tuple[pg.Rect, pg.Rect]:
            
                text (pg.Surface): Surface object containing
                "New game" rendered in BUTTON_FONT at
                BUTTON_FONT_SIZE px size
                textpos (pg.Rect): 'Rect' object containing the
                bounding rect of the text where it should be
        """
        
        global play_button_rect

        text = BUTTON_FONT.render("New game", True, (*BLACK, 255))
        y = exit_button_rect.top - 5 - Y_PADDING - text.get_height()
        textpos = text.get_rect(centerx=WIDTH/2, y=y)

        play_button_rect = pg.Rect(
            textpos[0] - X_PADDING,
            textpos[1] - Y_PADDING,
            textpos[2] + 2 * X_PADDING,
            textpos[3] + 2 * Y_PADDING
        )

        return (text, textpos)

    def focus_play_button() -> None:
        text, textpos = UI.generate_play_text()

        UI.draw_button_rect(play_button_rect, DIM_LIGHT_BLUE)
        screen.blit(text, textpos)
        pg.display.update(play_button_rect)

    def play_button_clicked() -> None:
        text, textpos = UI.generate_play_text()

        UI.draw_button_rect(play_button_rect, DARKENED_LIGHT_BLUE)
        screen.blit(text, textpos)
        pg.display.update(play_button_rect)

    def mouse_on_play_button() -> bool:
        return play_button_rect.contains((*pg.mouse.get_pos(), 0, 0))

    def draw_exit_button() -> None:
        # TODO: write docstring

        text, textpos = UI.generate_exit_text()

        UI.draw_button_rect(exit_button_rect, LIGHT_BLUE)
        screen.blit(text, textpos)
        pg.display.update(exit_button_rect)

    def generate_exit_text() -> tuple[pg.Rect, pg.Rect]:
        global exit_button_rect

        font = pg.font.Font(BUTTON_FONT_PATH, 36)
        text = font.render("Quit", True, (*BLACK, 255))
        centerx = WIDTH / 2
        y = HEIGHT - Y_PADDING - 5 - text.get_height()
        textpos = text.get_rect(centerx=centerx, y=y)
        exit_button_rect = pg.Rect(
            textpos[0] - X_PADDING,
            textpos[1] - Y_PADDING,
            textpos[2] + 2 * X_PADDING,
            textpos[3] + 2 * Y_PADDING
        )
        return (text, textpos)

    def focus_exit_button() -> None:
        text, textpos = UI.generate_exit_text()

        UI.draw_button_rect(exit_button_rect, DIM_LIGHT_BLUE)
        screen.blit(text, textpos)
        pg.display.update(exit_button_rect)

    def exit_button_clicked() -> None:
        text, textpos = UI.generate_exit_text()

        UI.draw_button_rect(exit_button_rect, DARKENED_LIGHT_BLUE)
        screen.blit(text, textpos)
        pg.display.update(exit_button_rect)

    def mouse_on_exit_button() -> bool:
        return exit_button_rect.contains((*pg.mouse.get_pos(), 0, 0))

    def draw_clear_button() -> None:
        text, textpos = UI.generate_clear_text()

        UI.draw_button_rect(clear_button_rect, LIGHT_BLUE)
        screen.blit(text, textpos)
        pg.display.update(clear_button_rect)

    def generate_clear_text() -> tuple[pg.Rect, pg.Rect]:
        global clear_button_rect

        font = pg.font.Font(BUTTON_FONT_PATH, 36)
        text = font.render("Clear", True, (*BLACK, 255))
        topleft = (
            WIDTH - X_PADDING - 5 - text.get_width(),
            HEIGHT - Y_PADDING - 5 - text.get_height()
        )
        textpos = text.get_rect(topleft=topleft)

        clear_button_rect = pg.Rect(
            textpos[0] - X_PADDING,
            textpos[1] - Y_PADDING,
            textpos[2] + 2 * X_PADDING,
            textpos[3] + 2 * Y_PADDING
        )

        return (text, textpos)

    def focus_clear_button() -> None:
        text, textpos = UI.generate_clear_text()

        UI.draw_button_rect(clear_button_rect, DIM_LIGHT_BLUE)
        screen.blit(text, textpos)
        pg.display.update(exit_button_rect)

    def clear_button_clicked() -> None:
        text, textpos = UI.generate_clear_text()

        UI.draw_button_rect(clear_button_rect, DARKENED_LIGHT_BLUE)
        screen.blit(text, textpos)
        pg.display.update(exit_button_rect)

    def mouse_on_clear_button() -> bool:
        return clear_button_rect.contains((*pg.mouse.get_pos(), 0, 0))

    def draw_note_button() -> None:
        text, textpos = UI.generate_note_text()

        UI.draw_button_rect(
            note_button_rect,
            LIGHT_BLUE if not note else LIGHT_PINK)
        screen.blit(text, textpos)
        pg.display.update(note_button_rect)

    def generate_note_text() -> tuple[pg.Rect, pg.Rect]:
        global note_button_rect

        font = pg.font.Font(BUTTON_FONT_PATH, 36)
        text = font.render("Note", True, (*BLACK, 255))
        topleft = (
            clear_button_rect.left + X_PADDING,
            clear_button_rect.top - 5 - Y_PADDING - text.get_height()
        )
        textpos = text.get_rect(topleft=topleft)

        note_button_rect = pg.Rect(
            textpos[0] - X_PADDING,
            textpos[1] - Y_PADDING,
            textpos[2] + 2 * X_PADDING,
            textpos[3] + 2 * Y_PADDING
        )

        return (text, textpos)

    def focus_note_button() -> None:
        text, textpos = UI.generate_note_text()

        UI.draw_button_rect(
            note_button_rect,
            DIM_LIGHT_BLUE if not note else DIM_LIGHT_PINK
        )
        screen.blit(text, textpos)
        pg.display.update(note_button_rect)

    def note_button_clicked() -> None:
        text, textpos = UI.generate_note_text()

        UI.draw_button_rect(
            note_button_rect,
            DARKENED_LIGHT_BLUE if not note else DARKENED_LIGHT_PINK
        )
        screen.blit(text, textpos)
        pg.display.update(note_button_rect)

    def mouse_on_note_button() -> None:
        return note_button_rect.contains((*pg.mouse.get_pos(), 0, 0))

    def win() -> None:
        global solved
        font = pg.font.Font(WIN_FONT_PATH, 48)
        text = font.render("You win!", True, BLACK)
        textpos = text.get_rect(centerx=WIDTH/2, centery=HEIGHT/2)
        screen.blit(text, textpos)
        solved = True


def play() -> None:
    global in_game, grid, note

    if in_game:
        UI.draw_game_buttons()
        N = 9
        K = randint(25, 30)
        grid = Grid(N, K)
        grid.fill_values()
        UI.generate_grid_rects()
        UI.draw_grid()

    note = False
    solved = False

    while not solved:  # TRY REMOVING WHILE LOOP
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            # TODO: send event to a handler function that saves screen.convert() to an array
            # for undo

            elif event.type == pg.MOUSEBUTTONUP:
                if UI.mouse_on_exit_button():
                    pg.quit()
                    quit()

                elif UI.mouse_on_play_button():
                    UI.focus_play_button()
                    in_game = True
                    play()

                elif not in_game:
                    continue

                elif UI.mouse_on_clear_button():
                    UI.focus_clear_button()
                    UI.clear()

                elif UI.mouse_on_note_button():
                    note = not note
                    UI.focus_note_button()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if UI.mouse_on_exit_button():
                    UI.exit_button_clicked()

                elif UI.mouse_on_play_button():
                    UI.play_button_clicked()

                elif not in_game:
                    continue

                elif UI.mouse_on_clear_button():
                    UI.clear_button_clicked()

                elif UI.mouse_on_note_button():
                    UI.note_button_clicked()

                elif UI.mouse_in_grid():
                    UI.select_cell()

            elif in_game and event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    if note:
                        UI.delete_num()
                    else:
                        UI.delete_num()

                if 49 <= event.key <= 57:
                    if note:
                        UI.toggle_note(int(pg.key.name(event.key)))
                    else:
                        UI.draw_num(int(pg.key.name(event.key)))

                elif event.key == 110:
                    UI.note_button_clicked()

            elif in_game and event.type == pg.KEYUP:
                if event.key == 110:
                    note = not note
                    sleep(0.05)
                    UI.draw_note_button()

            else:
                if UI.mouse_on_exit_button():
                    UI.focus_exit_button()
                else:
                    UI.draw_exit_button()

                if UI.mouse_on_play_button():
                    UI.focus_play_button()
                else:
                    UI.draw_play_button()

                if not in_game:
                    continue

                if UI.mouse_on_clear_button():
                    UI.focus_clear_button()
                else:
                    UI.draw_clear_button()

                if UI.mouse_on_note_button():
                    UI.focus_note_button()
                else:
                    UI.draw_note_button()
            if in_game:
                UI.focus_cell()


def main() -> None:
    global in_game
    in_game = False

    while True:
        play()


if __name__ == "__main__":
    # Initialize window
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption("Sudoku")

    # Create background
    UI.draw_menu()

    main()
