import random
from copy import deepcopy #Needed for creating a valid board
import pygame

class Tile:
    def __init__(self, value, x = 0, y = 0):
        self.value = value
        self.selected = False   # Highlight the tile border if selected == True
        self.is_problem = False # member variable to record whether the tile is initially given by the program
        self.user_input = 0   #Record the user input
        self.rect = pygame.Rect(x, y, 60, 60)  #Record the detail of every tile block

    def draw(self, screen, i, j):
        if self.selected == True: #If selected, highlight the border red
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
        if self.is_problem == True: #If the tile is part of the problem, display a grey number
            self.display(screen, self.value, (21+(j*60), (16+(i*60))), (119,136,153))

        if self.user_input == 0: # display a blank tile if user_input == 0
            pass                    
        elif self.user_input >= 1 and self.user_input <= 9:  # display a blue number if the input is between 1-9
            self.display(screen, self.user_input, (21+(j*60), (16+(i*60))), (0,0,255))
        elif self.user_input == 10:  # display a black number(self.value) if user_input == 10 (since the input has been verified)
            self.display(screen, self.value, (21+(j*60), (16+(i*60))), (0,0,0))
        
        

    def display(self, window, value, position, color): #Displays a number on the tile
        font = pygame.font.SysFont('lato', 45)
        text = font.render(str(value), True, color)
        window.blit(text, position)
    
class Board:
    def __init__(self):
        self.tiles = [ [Tile(0) for col in range(9)] for row in range(9) ]  #set all entries to zero
    
    def create_board(self, difficulty):
        #difficulty ranges from 1 to 10, easy to hard
        while True:
            for i in range(9):
                for j in range(9):
                    self.tiles[i][j].rect = pygame.Rect(60*j, 60*i, 60, 60) #Create each tile block in the correct position
                    self.tiles[i][j].is_problem = False #Initialize every tile to not be given
                    self.tiles[i][j].value = 0 #Reset the value at the start of each loop
            for row in range(9):
                for col in range(9):
                    if random.randint(1,10) > difficulty: #If a number generated is bigger than the difficulty, the tile will be given a value
                        self.tiles[row][col].value = random.randint(1,9)
                        if self.is_valid(self.tiles[row][col].value, row , col): #If the value works, it will be included in the problem
                            self.tiles[row][col].is_problem = True
                        else:
                            self.tiles[row][col].value = 0 #If it doesn't work, it will be left for user input
            tmp_board = deepcopy(self)

            if tmp_board.solve():
                return # when the board created is solvable, we continue with the rest of the program.
                       # If not, we will regenerate a new board

    def is_valid(self, value, row, col):
        #check rows
        for j in range(9):
            
            if self.tiles[row][j].value == value and j != col:
                return False
            
        #check columns
        for i in range(9):
            if self.tiles[i][col].value == value and i != row:
                return False

        #check every 3x3 matrix
        start_row = row - row%3
        start_col = col - col%3 
        for i in range(3):
            for j in range(3): 
                if self.tiles[start_row + i][start_col + j].value == value and (start_row + i != row or start_col + j != col):
                    return False #If in every matrix, there is another number who has the same value as the one we inputted, return false.
                
        
        return True #If nothing happens, the solution is valid, we return true.

    
    def set_tile(self, user_input, row, col): 
        if user_input == 0 or self.is_valid(user_input, row, col):
            self.tiles[row][col].value = user_input
            return True #Set the value of the tile to be the number we inputted
        else:
            return False
    

    def print_board(self):
        for row in range(9):
            if row % 3 == 0 and row != 0: #Print horizontal seperation lines
                print('- - - - - - - - - - - - - - - - - - - - - - - - -')
            for col in range(9):
                if col % 3 == 0 and col != 0: #Print vertical seperation lines
                    print(' | ' , end='')
                if col == 8:
                    print(self.tiles[row][col].value) #At the end of each row, print the value and go to the next row
                else:
                    print(str(self.tiles[row][col].value) + ' ', end= '') #For the other values, print the value and a gap

    def find_empty (self): #Find a empty tile for the solve algorithm
        for row in range(9):
            for col in range(9):
                if self.tiles[row][col].value == 0:
                    return (row, col)
        return None
    
    def solve(self):
        find = self.find_empty()
        if not find:
            return True #base case for recursion, if we don't find any empty tile, the current solution is valid.
        else:
            (row, col) = find
  
        for i in range(1,10):
            if self.is_valid(i, row, col): #at the empty tile, try every number from 1 to 9
                self.tiles[row][col].value = i #Set the empty tile to be the number in use
                if self.solve():
                    return True #Recursively calling the solve function, if there is a solution, return true
                self.tiles[row][col].value = 0 #If we didn't find a solution, reset the tile to 0 because it doesn't work

        return False #return false if we didn't find a solution

    def draw_board(self, screen):
        # Draws the whole board on the screen
        for i in range(9):
            for j in range(9):
                if j%3 == 0 and j != 0: #vertical lines
                    pygame.draw.line(screen, (0, 0, 0), ((j//3)*180, 0), ((j//3)*180, 540), 4)

                if i%3 == 0 and i != 0: #horizontal lines
                    pygame.draw.line(screen, (0, 0, 0), (0, (i//3)*180), (540, (i//3)*180), 4)

                self.tiles[i][j].draw(screen, i, j) #draw the tiles based on the draw function in the tile class
  
        #bottom-most line
        pygame.draw.line(screen, (0, 0, 0), (0, ((i+1) // 3) * 180), (540, ((i+1) // 3) * 180), 4)

    def select(self, mousePos):
        for row in range(9):
            for col in range(9):
                if self.tiles[row][col].is_problem: #if the tile is part of the problem, don't select
                    continue
                elif self.tiles[row][col].rect.collidepoint(mousePos): 
                    self.tiles[row][col].selected = True # Select the tile under mousePos
                else:
                    self.tiles[row][col].selected = False # deselect the other tiles
                    if self.tiles[row][col].user_input == 10:
                        pass #if the other values have been confirmed, pass
                    else:
                        self.tiles[row][col].user_input = 0 #if other inputs have not been confirmed, reset others.

def run_sudoku():
    pygame.init() 

    screen = pygame.display.set_mode( (540, 540) ) #set the play screen

    pygame.display.set_caption("Sudoku Solver")
    icon = pygame.image.load("numbers-6-6.jpg")
    pygame.display.set_icon(icon) #game name and icon

    board = Board()
    board.create_board(5)

    running = True
    while running: #The game runs as long as running is true.
        screen.fill((255, 255, 255)) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False #If we close the window, the game ends

            elif event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                board.select(mousePos) #when we release the mouse click, the tile that is under the cursor is selected
                
            elif event.type == pygame.KEYDOWN:
                no_tile_selected = True
                sel_row, sel_col = -1, -1 #default position of the selected tile
                
                
                for i in range(9):
                    for j in range(9):
                        if board.tiles[i][j].selected:
                            no_tile_selected = False
                            sel_row, sel_col = i, j #store the position of the selected tile
                
                # K_S (solve and show the final answer)
                if event.key == pygame.K_s:
                    board.solve()
                    # display all the tiles in black
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].user_input = 10

                #do nothing if user presses the keyboard without selecting any tile
                if no_tile_selected:
                    continue    
                
                # number keys
                if event.key == pygame.K_1:
                    board.tiles[sel_row][sel_col].user_input = 1

                if event.key == pygame.K_2:
                    board.tiles[sel_row][sel_col].user_input = 2

                if event.key == pygame.K_3:
                    board.tiles[sel_row][sel_col].user_input = 3

                if event.key == pygame.K_4:
                    board.tiles[sel_row][sel_col].user_input = 4

                if event.key == pygame.K_5:
                    board.tiles[sel_row][sel_col].user_input = 5

                if event.key == pygame.K_6:
                    board.tiles[sel_row][sel_col].user_input = 6

                if event.key == pygame.K_7:
                    board.tiles[sel_row][sel_col].user_input = 7

                if event.key == pygame.K_8:
                    board.tiles[sel_row][sel_col].user_input = 8

                if event.key == pygame.K_9:
                    board.tiles[sel_row][sel_col].user_input = 9

                # backspace/delete
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    board.tiles[sel_row][sel_col].user_input = 0

                # Enter
                if event.key == pygame.K_RETURN:
                    if board.tiles[sel_row][sel_col].user_input == 0:
                        # Do nothing if the user hasn't pressed a number key
                        pass
                    else:
                        if board.set_tile(board.tiles[sel_row][sel_col].user_input, sel_row, sel_col): #set the tile to be the value we inputted
                            board.tiles[sel_row][sel_col].user_input = 10   # set input to 10, suggesting the tile has been modified by the user
                        else:
                            board.tiles[sel_row][sel_col].user_input = 0 #if the input is not possible, reset the user input
                        board.tiles[sel_row][sel_col].selected = False #the tile is no longer selected

        board.draw_board(screen)
        pygame.display.update()

run_sudoku()

