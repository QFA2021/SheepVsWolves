import abc


class Piece(abc.ABC):
    
    # General values for all pieces:
    # - getImage()
    # - movement
    # abstract Movement
    @abc.abstractmethod
    def isValid(xFrom, yFrom, xTo, yTo):
        pass
        
        
class Sheep(Piece):
    pass
    # Create methods and variables for
    # - entangled
    # - superposition
    # - image depending on superposition / entanglement
    # - specific movement
    

    
class Wolf(Piece):
    # - specific Image
    # - specific movement
    pass