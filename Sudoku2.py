"""Sudoku Game

This script allows the user to play Sudoku, or run a backtracking algorithm to autosolve.\
It is assumed that the user's screen has a resolution of 650x720 or higher.

The script requires that `pygame` be installed within the Python environment you are running\
it in.

The file can be imported as a module and contains the following functions:

    * clear_grid - clears the play area for a new game
    * write_to_grid - writes a number to a space in the grid
    * write_note_to_grid - writes a note to a space in the grid
    * """ # TODO: finish Docstring header
# Import Modules
from random import randint, shuffle
import math
import pygame as pg
from time import sleep

if not pg.font:
    print("Warning, fonts disabled")
    
# Define constants
WHITE = 255, 255, 255
BLACK = 10, 10, 10
DARK_GRAY = 69, 67, 66
GRAY = 209, 206, 197
DIM_GRAY = 171, 171, 164
LIGHT_BLUE = 69, 218, 255
DIM_LIGHT_BLUE = 64, 203, 237
DARKENED_LIGHT_BLUE = 60, 188, 219
PINK = 245, 66, 129
DIM_PINK = 222, 55, 114
DARKENED_PINK = 196, 47, 100
SIZE = WIDTH, HEIGHT = 650, 720
X_PADDING, Y_PADDING = 15, 5
GRID_DIMENSION = 4 * WIDTH / 5
BOX_SIZE = GRID_DIMENSION / 9
NUM_FONT = pg.font.match_font("americantypewriter")
NOTE_FONT = pg.font.match_font("farah")
BUTTON_FONT = pg.font.match_font("courier")
MAIN_FONT = pg.font.match_font("pingfang")

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
        self.selected = (-1, -1)
        self.N = N
        self.K = K
        
        self.notes = [[[0 for _ in range(N)] for _ in range(N)] for _ in range(N)]
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
        
        for curr_x in range(left, left + self.sqrt_N):
            for curr_y in range(top, top + self.sqrt_N):
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
                
    def write_num(self, num:int, x:int, y:int)->None:
        """Inserts a number in the playing grid.

        Args:
            x (int): x coordinate to insert number (1-N)
            y (int): y coordinate to insert number (1-N)
            num (int): number to add (1-N)
        """
        self.grid[y][x] = num
        
    def remove_num(self, x:int, y:int)->None:
        """Removes a number from the playing grid.

        Args:
            x (int): x coordinate to remove number (1-N)
            y (int): y coordinate to remove number (1-N)
        """
        self.grid[y][x] = 0
        
    # TODO: Finish write_note_to_grid method
    def write_note(self, x:int, y:int, num:int)->None:
        """Writes a note to a space on the grid.
    
        Args:
            num (int): The number to write
            pos (tuple(int)): The coordinates (x, y) of the space in
            the NxN grid to be written to
        """
        self.notes[y][x][num - 1] = 1
        
    def remove_note(self, x:int, y:int, num:int)->None:
        self.notes[y][x][num - 1] = 0
    
    def get_notes_from_cell(self, x:int, y:int)->list[int]:
        return self.notes[x][y]
    
    def get_grid(self)->tuple[int, int]:
        return self.grid
    
    def get_N(self)->int:
        return self.N
    
    def get_selected_cell(self)->tuple[int, int]:
        return self.selected
    
    def set_selected_cell(self, selected:tuple[int, int])->None:
        self.selected = selected
        
    def get_solution(self)->list[list[int]]:
        return self.solution
                    
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
                output += ("+" + "-" * (3 * self.sqrt_N)) * self.sqrt_N + "+"
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
    
class UI(object):
    # TODO: write docstring
    
    def draw_menu()->None:
        global background
        background = pg.Surface(SIZE).convert_alpha()
        background.fill((*WHITE, 255))
        
        UI.generate_blank_grid()
        UI.draw_background()
        
    def draw_background()->None:
        UI.draw_header()
        UI.draw_menu_buttons()
        
        screen.blit(background, (0, 0))
        pg.display.flip()
    
    def draw_header()->None:
        #TODO: write docstring
        
        global header_rect_bottom
        
        font = pg.font.Font(MAIN_FONT, 36)
        text = font.render("Play Sudoku or Let the Computer Play", True, BLACK)
        y = 10
        textpos = text.get_rect(centerx=WIDTH/2, y=y)
        header_rect_bottom = textpos.height + y
        background.blit(text, textpos)
            
    def update_screen()->None:
        pass
        
    def generate_blank_grid()->None:
        # TODO: write docstring
        
        global blank_grid, grid_rects
        grid_rects = []
        blank_grid = pg.Surface((GRID_DIMENSION+3, GRID_DIMENSION+3)).convert_alpha()
        blank_grid.fill((*WHITE, 0))
                
        for i in range(10):
            line_width = 3 if i % 3 == 0 or i == 0 else 1
                
            pg.draw.line( # draw vertical lines
                blank_grid,
                (*BLACK, 255),
                (i * BOX_SIZE + 1, 0), 
                (i * BOX_SIZE + 1, 9 * BOX_SIZE + 2),
                line_width
                )
            pg.draw.line( # draw horizontal lines
                blank_grid,
                (*BLACK, 255),
                (0, i * BOX_SIZE + 1),
                (9 * BOX_SIZE + 2, i * BOX_SIZE + 1),
                line_width
            )

    def update_grid()->None:
        UI.draw_blank_grid()
        
        grid_pos = UI.get_grid_pos()
        grid_x, grid_y = grid_pos[0], grid_pos[1] - 12 # TODO: find proportional way to do this
        box_size = BOX_SIZE - 1
        font = pg.font.Font(NUM_FONT, 48)
        
        for i, row in enumerate(grid.get_grid()):
            grid_y += 1
            x = grid_x
            
            row_rects = []
            for j, n in enumerate(row):
                x += 1
                y = (grid_y -
                     font.get_ascent() +
                     ((i + 1) * box_size))
                row_rects.append(pg.Rect(x + j * box_size, y - 1, box_size + 2, box_size + 2))
                
                if n == 0:
                    continue
                
                if grid.check_if_given(j, i):
                    font.set_bold(True)
                else:
                    font.set_bold(False)
                
                num_text = font.render(str(n), True, BLACK)
                centerx = x + (j * box_size + (j + 1) * box_size) / 2
                num_pos = num_text.get_rect(centerx=centerx, y=y)
                screen.blit(num_text, num_pos)
            grid_rects.append(row_rects)
        
        pg.display.update(blank_grid.get_rect(topleft=UI.get_grid_pos()))
        
    def draw_blank_grid()->None:
        screen.blit(blank_grid, UI.get_grid_pos())
        
    def focus_grid_square()->None:
        x, y = UI.get_square_from_mouse()
        
        if not grid.check_if_given(x, y):
            pg.draw.rect(screen, GRAY, grid_rects[y][x], 0)
            
        if grid.get_selected_cell() != (-1, -1):
            UI.select_grid_square(grid.get_selected_cell())
        UI.update_grid()
        pg.display.update(grid_rects[y][x])
    
    def select_grid_square(pos:tuple[int, int]=None)->None:
        x, y = pos if pos else UI.get_square_from_mouse()
        
        if not grid.check_if_given(x, y):
            pg.draw.rect(screen, DIM_GRAY, grid_rects[y][x], 0)
            grid.set_selected_cell((x, y))
        UI.update_grid()
        pg.display.update(grid_rects[y][x]) 
    
    def draw_num(n:int)->None:
        col, row = grid.get_selected_cell()
        if (col, row) == (-1, -1):
            return
        
        grid.write_num(int(n), col, row)
        
        UI.update_grid()
        
        if grid.is_solved():
            UI.win()
            
    def delete_num()->None:
        col, row = grid.get_selected_cell()
        if (col, row) == (-1, -1):
            return
        
        grid.remove_num(col, row)
        #grid.set_selected((-1, -1))
        UI.update_grid()
    
    def draw_note(num:int)->None: # USE FARAH font
        col, row = grid.get_selected_cell()
    
    def delete_note()->None:
        pass
    
    def mouse_in_grid()->bool:
        left, top = UI.get_grid_pos()
        return blank_grid.get_rect(
            topleft=(left+3, top+3),
            width=blank_grid.get_width() - 6,
            height=blank_grid.get_height() - 6
            ).contains((*pg.mouse.get_pos(), 0, 0))
    
    def get_square_from_mouse()->tuple[int, int]:
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
        
    def get_grid_pos()->tuple[int|float, int|float]:
        x = (WIDTH - blank_grid.get_rect().width) / 2
        y = header_rect_bottom + ((play_button_rect.top - header_rect_bottom - blank_grid.get_rect().height) / 2)
        return (x, y)
                
    def draw_menu_buttons()->None:
        #TODO: write docstring
        
        UI.draw_exit_button()
        UI.draw_play_button()
        
    def draw_game_buttons()->None:
        UI.draw_clear_button()
        UI.draw_note_button()
                
    def draw_button_rect(surface:pg.Surface, rect:pg.Rect, color:tuple[int, int, int])->None:
        pg.draw.rect(surface, color, rect, 0, 3)
    
    def draw_play_button()->None:
        #TODO write docstring
                
        text, textpos = UI.generate_play_text()
        
        UI.draw_button_rect(background, play_button_rect, LIGHT_BLUE)
        background.blit(text, textpos)
        pg.display.update(play_button_rect)
            
    def generate_play_text()->tuple[pg.Rect, pg.Rect]:
        global play_button_rect
        
        font = pg.font.Font(BUTTON_FONT, 36)
        text = font.render("New game", True, (*BLACK, 255))
        y = exit_button_rect.top - 5 - Y_PADDING - text.get_height()
        textpos = text.get_rect(centerx=WIDTH/2, y=y)
        
        play_button_rect = pg.Rect(
            textpos[0] - X_PADDING,
            textpos[1] - Y_PADDING,
            textpos[2] + 2 * X_PADDING,
            textpos[3] + 2 * Y_PADDING
        )
        
        return (text, textpos)
            
    def focus_play_button()->None:
        text, textpos = UI.generate_play_text()
        
        UI.draw_button_rect(background, play_button_rect, DIM_LIGHT_BLUE)
        background.blit(text, textpos)
        pg.display.update(play_button_rect)
        
    def play_button_clicked()->None:
        text, textpos = UI.generate_play_text()
        
        UI.draw_button_rect(background, play_button_rect, DARKENED_LIGHT_BLUE)
        background.blit(text, textpos)
        pg.display.update(play_button_rect)
        
    def mouse_on_play_button()->bool:
        return play_button_rect.contains((*pg.mouse.get_pos(), 0, 0))
        
    def draw_exit_button()->None:
        #TODO: write docstring
        
        text, textpos = UI.generate_exit_text()
        
        UI.draw_button_rect(background, exit_button_rect, LIGHT_BLUE)
        background.blit(text, textpos)
        pg.display.update(exit_button_rect)
        
    def generate_exit_text()->tuple[pg.Rect, pg.Rect]:
        global exit_button_rect
        
        font = pg.font.Font(BUTTON_FONT, 36)
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
                    
    def focus_exit_button()->None:
        text, textpos = UI.generate_exit_text()
        
        UI.draw_button_rect(background, exit_button_rect, DIM_LIGHT_BLUE)
        background.blit(text, textpos)
        pg.display.update(exit_button_rect)
    
    def exit_button_clicked()->None:
        text, textpos = UI.generate_exit_text()
        
        UI.draw_button_rect(background, exit_button_rect, DARKENED_LIGHT_BLUE)
        background.blit(text, textpos)
        pg.display.update(exit_button_rect)
    
    def mouse_on_exit_button()->bool:
        return exit_button_rect.contains((*pg.mouse.get_pos(), 0, 0))
    
    def draw_clear_button()->None:
        text, textpos = UI.generate_clear_text()
        
        UI.draw_button_rect(screen, clear_button_rect, LIGHT_BLUE)
        screen.blit(text, textpos)
        pg.display.update(clear_button_rect)
        
        UI.draw_button_rect(background, clear_button_rect, LIGHT_BLUE)
        background.blit(text, textpos)

    
    def generate_clear_text()->tuple[pg.Rect, pg.Rect]:
        global clear_button_rect
        
        font = pg.font.Font(BUTTON_FONT, 36)
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
    
    def focus_clear_button()->None:
        text, textpos = UI.generate_clear_text()
        
        UI.draw_button_rect(background, clear_button_rect, DIM_LIGHT_BLUE)
        background.blit(text, textpos)
        pg.display.update(exit_button_rect)
    
    def clear_button_clicked()->None:
        text, textpos = UI.generate_clear_text()
        
        UI.draw_button_rect(background, clear_button_rect, DARKENED_LIGHT_BLUE)
        background.blit(text, textpos)
        pg.display.update(exit_button_rect)
    
    def mouse_on_clear_button()->bool:
        return clear_button_rect.contains((*pg.mouse.get_pos(), 0, 0))
    
    def clear()->None:
        for i in range(0, grid.get_N()):
            for j in range(0, grid.get_N()):
                if not grid.check_if_given(i, j):
                    grid.remove_num(i, j)
                    
        grid.set_selected_cell((-1, -1))
        UI.update_grid()
        
    def draw_note_button()->None:
        text, textpos = UI.generate_note_text()
        
        UI.draw_button_rect(
            screen,
            note_button_rect,
            LIGHT_BLUE if not note else PINK)
        screen.blit(text, textpos)
        pg.display.update(note_button_rect)
        
        UI.draw_button_rect(
            background,
            note_button_rect,
            LIGHT_BLUE if not note else PINK)
        background.blit(text, textpos)
        
    def generate_note_text()->tuple[pg.Rect, pg.Rect]:
        global note_button_rect
        
        font = pg.font.Font(BUTTON_FONT, 36)
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
    
    def focus_note_button()->None:
        text, textpos = UI.generate_note_text()
        
        UI.draw_button_rect(
            screen,
            note_button_rect,
            DIM_LIGHT_BLUE if not note else DIM_PINK
            )
        screen.blit(text, textpos)
        pg.display.update(note_button_rect)
        
        UI.draw_button_rect(
            background,
            note_button_rect,
            DIM_LIGHT_BLUE if not note else DIM_PINK)
        background.blit(text, textpos)
    
    def note_button_clicked()->None:
        text, textpos = UI.generate_note_text()
        
        '''UI.draw_button_rect(
            screen,
            note_button_rect,
            DARKENED_LIGHT_BLUE if not note else DARKENED_PINK
        )
        screen.blit(text, textpos)
        pg.display.update(note_button_rect)'''
        
        UI.draw_button_rect(
            background,
            note_button_rect,
            DARKENED_LIGHT_BLUE if not note else DARKENED_PINK)
        background.blit(text, textpos)
        #screen.blit(background, (0, 0))
        pg.display.update(note_button_rect)
    
    def mouse_on_note_button()->None:
        return note_button_rect.contains((*pg.mouse.get_pos(), 0, 0))
    
    def win()->None:
        font_path = pg.font.match_font('menlo', True)
        font = pg.font.Font(font_path, 48)
        text = font.render("You win!", True, BLACK)
        textpos = text.get_rect(centerx=WIDTH/2, centery=HEIGHT/2)
        screen.blit(text, textpos)
        solved = True
        
def play()->None:
    global in_game, grid, note
    
    if in_game:
        UI.draw_game_buttons()
        N = 9
        K = randint(25, 30)
        grid = Grid(N, K)
        grid.fill_values()
                
        UI.update_grid()
    
    note = False
    solved = False
    
    while not solved:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
                
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
                    UI.focus_note_button()
                    note = not note
                    
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
                    UI.select_grid_square()
                    
            elif event.type == pg.KEYDOWN:
                if not in_game:
                    continue
                
                if not note and event.key == pg.K_BACKSPACE:
                    UI.delete_num()
                    
                if 49 <= event.key <= 57:
                    if note:
                        UI.draw_note(int(pg.key.name(event.key)))
                    else:
                        UI.draw_num(int(pg.key.name(event.key)))
                elif event.key == 3:
                    UI.note_button_clicked()
                    sleep(0.2)
                    UI.focus_note_button()
                    note = not note
                    
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
                                    
                if UI.mouse_in_grid():
                    UI.focus_grid_square()
                elif grid.get_selected_cell() != (-1, -1):
                    UI.select_grid_square(grid.get_selected_cell())
                else:
                    UI.update_grid()
        
        screen.blit(background, (0, 0))
                    
def main()->None:
    global in_game
    in_game = False
    
    while True:
        play()
        
if __name__ == "__main__":
    # Initialize window
    pg.init()
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption("Sudoku")

    # Create background
    UI.draw_menu()
    
    # Run game
    main()