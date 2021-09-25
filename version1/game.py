# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 09:16:36 2021

@author: Elias, Jan, Martin
"""
from pieces import Sheep, Wolf
import enum
import pieces.py

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
                if not isOutside(x ,y):
                    self.gameboard[x][y] = Sheep()
                
               
        # add wolfs
        self.gameboard[4][2] = Wolf()
        self.gameboard[4][4] = Wolf()
        
        
    def is_clickable(self, x: int, y: int) -> bool:
        if self.state == TurnState.selecting:
            return not self.isEmpty(x, y)
        
        selected_piece = self.get_selected_piece()
        
        return selected_piece.isValid(self.selected_x, self.selected_y, x, y)
        
    
    def get_selected_piece(self) -> pieces.Piece:
        return self.gameboard[self.selected_x][self.selected_y]


    # Performs the action according to the current game state
    # Attention:    Before calling this method, check whether this point is 
    #               clickable!
    def click_action(self, x: int, y: int):
        if self.state == TurnState.selecting:
            self.selected_x = x
            self.selected_y = y
                        
        elif self.state == TurnState.moving:
            piece = self.get_selected_piece()
            
            if type(piece) is Sheep:
                self.move_sheep(piece, x, y)
            elif type(piece) is Wolf:
                self.move_wolf(piece, x, y)
            
            
        self.update_state()
        
    def update_state(self):
        if self.state == TurnState.selecting:
            self.state = TurnState.moving
        elif self.state == TurnState.moving:
            self.state = TurnState.selecting
            
        if self.sheep_in_stable >= 9 or self.sheep_left < 9:
            self.state = TurnState.over
    

    def move_sheep(self, sheep: Sheep, x: int, y: int):
        move_piece_simple(sheep, x, y)
        
        if is_in_stable(x, y):
            self.sheep_safe += 1


    def move_wolf(self, wolf: Wolf, x: int, y: int):
        move_piece_simple(wolf, x, y)

        # TODO: temporary, check this later with method provided by gui
        normal_move = True  
        if not normal_move:
            # A capture move was made, so a sheep has been captured
            in_between_x = (x + self.selected_x) / 2
            in_between_y = (y + self.selected_y) / 2
            
            self.gameboard[in_between_x][in_between_y] = None
            self.sheep_left -= 1
            
            # Sheep in the stable has been eaten
            if is_in_stable(in_between_x, in_between_y):
                self.sheep_in_stable -= 1
            
            
    def move_piece_simple(self, piece: pieces:Piece, x: int, y: int): 
        self.gameboard[self.selected_x][self.selected_y()] = None
        self.gameboard[x][y] = piece
    


    
    
    def isEmpty(self, x, y) -> bool:
        if not self.isOutside(x, y):
            return self.gameboard[x][y] == None
        return False
        
    
def is_in_stable(x: int, y: int) -> bool:
    if y < 4: return False    
    if x < 2 or x > 4: return False
    return True
    
def isOutside(x, y) -> bool:
        if 0 <= y <= 1 or 5 <= y <= 6:
            if 0 <= x <= 1 or 5 <= x <= 6:
                return True
        elif 2 <= y <= 4:
            if 0 <= x <= 6:
                return True

        return False   
        