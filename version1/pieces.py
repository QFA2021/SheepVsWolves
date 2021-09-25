# -*- coding: utf-8 -*-
import abc
import os
import game.py

class Piece(abc.ABC):
    # General values for all pieces:
    # getImage() - check mate
    # abstract Movement
    @abc.abstracmethod
    def getImage():
        pass
    
    @abc.abstractmethod
    def isValid(xFrom, yFrom, xTo, yTo):
        pass
        
class Sheep(Piece):
    def getImage():
        return os.path.join("/icons/sheep.png")
    
    def isValid(xFrom, yFrom, xTo, yTo):
        free = game.isFree(xTo, yTo)
        if free==False:
            return False
        #check sheep going down
        down = (yTo >= yFrom)
        #check step length
        dist_square = (xTo-xFrom)^2 + (yTo-yFrom)^2
        if down and (dist_square <= 2):
            return True
        return False
    
    
    # Create methods and variables for
    # - entangled
    # - superposition
    # - image depending on superposition / entanglement
    # - specific movement
    
class Wolf(Piece):
    def getImage():
        return os.path.join("/icons/wolf.png")
    
    
    # - specific Image
    # - specific movement