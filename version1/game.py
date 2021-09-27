# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 09:16:36 2021

@author: Elias, Jan, Martin
"""
from pieces import Sheep, Wolf
import enum
import pieces

# The state indicates which action is next to be performed
class TurnState(enum.Enum):
    selecting = 1
    moving = 2
    
    # Tracks whether the game is over. This is the case if ether there are
    # less than 9 sheep left or the stable is full
    over = 3
    
class Game:
    
    gameboard = []
    
    # Store the placement of the pieces
    def __init__(self):    
        self.sheep_in_stable = 0
        self.sheep_left = 20
        
        # Indicating whether its the sheep players or the wolfs turn
        self.sheeps_turn = True
        # Currently in the first phase of a turn; selecting a piece to move
        self.state = TurnState.selecting
        
        self.selected_x = -1
        self.selected_y = -1
        
        self.init_gameboard()
            
            
    def init_gameboard(self):
        self.gameboard = [[None for x in range (7)] for y in range (7)]
        
        # add sheep
        for y in range(4):
            for x in range(7):
                if not is_outside(x,y):
                    self.gameboard[x][y] = Sheep()
                
               
        # add wolfs
        self.gameboard[2][4] = Wolf()
        self.gameboard[4][4] = Wolf()
        
        
    def is_clickable(self, x: int, y: int) -> bool:
        # SELECTING
        if self.state == TurnState.selecting:
            if self.is_empty(x, y):
                return False
            
            piece = self.gameboard[x][y]
            if self.sheeps_turn:
                return type(piece) == Sheep
            else:
                return type(piece) == Wolf
        
        # MOVING
        selected_piece = self.get_selected_piece()
        if not self.is_empty(x, y):
            return False
        
        valid = selected_piece.is_move_valid(self.selected_x, self.selected_y, x, y)
        print (f"is move to {x},{y} valid {valid}")
        return valid
        
    
    def get_selected_piece(self) -> pieces.Piece:
        return self.gameboard[self.selected_x][self.selected_y]


    # Performs the action according to the current game state
    # Attention:    Before calling this method, check whether this point is 
    #               clickable!
    def click_action(self, x: int, y: int):
        # SELECTING
        if self.state == TurnState.selecting:
            self.selected_x = x
            self.selected_y = y
            print (f"{x},{y} selected")
             
        # MOVING
        elif self.state == TurnState.moving:
            piece = self.get_selected_piece()
            
            if type(piece) is Sheep:
                self.move_sheep(piece, x, y)
            elif type(piece) is Wolf:
                self.move_wolf(piece, x, y)
                
            self.deselect()
            
            
        self.update_state()
        
        
    def deselect(self):
        self.selected_x = -1
        self.selected_y = -1
        
    def update_state(self):
        if self.state == TurnState.selecting:
            self.state = TurnState.moving
        elif self.state == TurnState.moving:
            self.state = TurnState.selecting
            self.sheeps_turn = not self.sheeps_turn
            
        if self.sheep_in_stable >= 9:
            self.state = TurnState.over
            print("Sheep won!")

        if self.sheep_left < 9:
            self.state = TurnState.over
            print ("Wolf won!")
            
        
    

    def move_sheep(self, sheep: Sheep, x: int, y: int):
        self.move_piece_simple(sheep, x, y)
        
        if is_in_stable(x, y):
            self.sheep_in_stable += 1
            
        print (f"sheep moved to {x},{y}")


    def move_wolf(self, wolf: Wolf, x: int, y: int):
        self.move_piece_simple(wolf, x, y)

        capture = False
        if abs(x - self.selected_x) == 2 or abs(y - self.selected_y) == 2:
            capture = True
        
        if capture:
            # A capture move was made, so a sheep has been captured
            in_between_x = (x + self.selected_x) // 2
            in_between_y = (y + self.selected_y) // 2
            
            self.gameboard[in_between_x][in_between_y] = None
            self.sheep_left -= 1
            
            # Sheep in the stable has been eaten
            if is_in_stable(in_between_x, in_between_y):
                self.sheep_in_stable -= 1
                
            print (f"wolf moved to {x},{y}")

            
            
    def move_piece_simple(self, piece: pieces.Piece, x: int, y: int): 
        self.gameboard[self.selected_x][self.selected_y] = None
        self.gameboard[x][y] = piece
    


    
    
    def is_empty(self, x, y) -> bool:
        if not is_outside(x, y):
            return self.gameboard[x][y] == None
        return False
        
    
def is_in_stable(x: int, y: int) -> bool:
    if y < 4: return False    
    if x < 2 or x > 4: return False
    return True
    
def is_outside(x: int, y: int) -> bool:
    if (x<0 or x>6): return True
    if (y<0 or y>6): return True    
    if y<2 or y>4:
        if x<2 or x>4:
            return True
    return False   

# whether two points are connected on the gameboard via the grid
def is_connected(x1: int, y1: int, x2: int, y2: int) -> bool:
    if x1 == x2 and y1 == y2:
        return False
    
    if (x1 - x2)**2 + (y1 - y2)**2 > 2:
        return False
    
    if is_outside(x1, y1) or is_outside(x2, y2):
        return False
    
    return is_connected_straight(x1, y1, x2, y2) or is_connected_diagonally(x1, y1, x2, y2)
    
    
def is_connected_straight(x1: int, y1: int, x2: int, y2: int) -> bool:
    return (abs(x1 - x2) == 1) != (abs(y1 - y2) == 1)

    

def is_connected_diagonally(x1: int, y1: int, x2: int, y2: int) -> bool:
    return (x1 - y1) % 2 == 0 and (x2 - y2) % 2 == 0
    