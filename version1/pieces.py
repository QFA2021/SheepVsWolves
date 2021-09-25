# -*- coding: utf-8 -*-

class Piece:
    
    # General values for all pieces:
    # - getImage()
    # - movement
    
    def __init__(x , y):
        self.x = x
        self.y = y
        
    # abstract Movement
    @abstractmethod
    def isValid(xFrom, yFrom, xTo, yTo):
        
        
class Sheep(Piece):
    # Create methods and variables for
    # - entangled
    # - superposition
    # - image depending on superposition / entanglement
    # - specific movement
    
    
class Wolf(Piece):
    # - specific Image
    # - specific movement