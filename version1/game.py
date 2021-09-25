# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 09:16:36 2021

@author: Elias, Jan, Martin
"""
from pieces import Sheep, Wolf


class Game:
    
    gameboard = []
    
    # Store the placement of the pieces
    def __init__(self):
        self.initGameboard()
            
            
    def initGameboard(self):
        self.gameboard = [[None for x in range (7)] for y in range (7)]
        
        # add sheep
        for y in range(4):
            for x in range(7):
                if not self.isOutside(x ,y):
                    self.gameboard[x][y] = Sheep()
                
               
        # add wolfs
        self.gameboard[4][2] = Wolf()
        self.gameboard[4][4] = Wolf()

    
    
    
    # Store the state of the game 
    # - whos turn it is
    # - game over
    # - which piece is selected
    
    # methods:
    # - isEmtpy()
    # - isOutSide() / isInside()
    def isEmpty(self, x, y) -> bool:
        if not self.isOutside(x, y):
            return self.gameboard[x][y] == None
        return False
        
    def isOutside(x, y) -> bool:
        if y < 2:
            if x < 2 or x > 4:
                return True
        elif y > 4:
            if x < 2 or x > 4:
                return True
            
        return False
        