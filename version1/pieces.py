import abc
import game

class Piece(abc.ABC):
    def get_image(self):
        pass
    
    def is_move_valid(gameboard, xFrom, yFrom, xTo, yTo):
        pass
        
class Sheep(Piece):
    def get_image(self):
        return "icons/cute_sheep_transparent.png"
    
    def is_move_valid(self, gameboard, xFrom :int, yFrom :int, xTo :int, yTo :int) -> bool:
        #check sheep going down
        down = (yTo >= yFrom)
        #check connection
        if game.is_connected(xFrom,yFrom,xTo,yTo) and down:
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
    def get_image(self):
        return "icons/wolf_transparent.png"
            
    def is_move_valid(self, gameboard, xFrom :int, yFrom :int, xTo :int, yTo :int) -> bool:
        if not self.is_capture_move(xFrom, yFrom, xTo, yTo):
            return game.is_connected(xFrom, yFrom, xTo, yTo)

        in_between_x = (xFrom + xTo) // 2
        in_between_y = (yFrom + yTo) // 2
        piece = gameboard[in_between_x][in_between_y]
        return type(piece) == Sheep

    def is_capture_move(self, xFrom :int, yFrom :int, xTo :int, yTo :int) -> bool:
        length_sq = (xFrom - xTo)**2 + (yFrom - yTo)**2
        #             straight      diagonal
        if not (length_sq == 4 or length_sq == 8):
            return False

        in_between_x = (xFrom + xTo) // 2
        in_between_y = (yFrom + yTo) // 2

        connected1 = game.is_connected(xFrom, yFrom, in_between_x, in_between_y)
        connected2 = game.is_connected(in_between_x, in_between_y, xTo, yTo)

        return connected1 and connected2