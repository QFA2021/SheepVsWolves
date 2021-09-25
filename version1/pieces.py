# -*- coding: utf-8 -*-
import abc


class Piece(abc.ABC):
    
    # General values for all pieces:
    # - getImage()
    # - movement
    # abstract Movement
    @abc.ABC.abstractmethod
    def isValid(xFrom, yFrom, xTo, yTo):
        
        
class Sheep(Piece):
    # Create methods and variables for
    # - entangled
    # - superposition
    # - image depending on superposition / entanglement
    # - specific movement
    pass
    
class Wolf(Piece):
    # - specific Image
    # - specific movement