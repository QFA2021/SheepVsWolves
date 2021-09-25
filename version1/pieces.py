import abc
import os

class Piece(abc.ABC):
    def getImage(self):
        pass
    
    def isValid(xFrom, yFrom, xTo, yTo):
        pass
        
class Sheep(Piece):
    def getImage(self):
        return "icons/cute_sheep_transparent.png"
    
    def isValid(xFrom :int, yFrom :int, xTo :int, yTo :int) -> bool:
        #check sheep going down
        down = (yTo <= yFrom)
        #check step length
        dist_square = (xTo-xFrom)**2 + (yTo-yFrom)**2
        if down and (dist_square==1 or dist_square==2):
            return True
        return False
    
    ENTANGLED = False
    SUPERPOSITION = False
    # Create methods and variables for
    # - entangled
    # - superposition
    # - image depending on superposition / entanglement
    # - specific movement

    
class Wolf(Piece):
    def getImage(self):
        return "icons/wolf_transparent.png"
            
    def isValid(xFrom :int, yFrom :int, xTo :int, yTo :int) -> bool:
        #check step length
        dist_square = (xTo-xFrom)**2 + (yTo-yFrom)**2
        if (dist_square==1 or dist_square==2 or dist_square==4 or dist_square==8):
            return True
        return False