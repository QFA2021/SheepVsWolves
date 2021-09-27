import abc
import pathlib
import game


class Piece(abc.ABC):
    def get_image(self):
        pass
    
    def is_move_valid(gameboard, x_from, y_from, x_to, y_to):
        pass
        
        
class Sheep(Piece):

    def __init__(self):
        self.entanglement_id = -1

    def get_image(self):
        path = pathlib.Path().resolve()
        return f"{path}/version1/icons/cute_sheep_transparent.png"
    
    def is_move_valid(self, gameboard, x_from: int, y_from: int, x_to: int, y_to: int) -> bool:
        # check sheep going down
        down = (y_to >= y_from)
        # check connection
        if game.is_connected(x_from, y_from, x_to, y_to) and down:
            return True
        return False


def is_capture_move(x_from :int, y_from :int, x_to :int, y_to :int) -> bool:
    length_sq = (x_from - x_to)**2 + (y_from - y_to)**2
    #             straight      diagonal
    if not (length_sq == 4 or length_sq == 8):
        return False

    in_between_x = (x_from + x_to) // 2
    in_between_y = (y_from + y_to) // 2

    connected1 = game.is_connected(x_from, y_from, in_between_x, in_between_y)
    connected2 = game.is_connected(in_between_x, in_between_y, x_to, y_to)

    return connected1 and connected2


class Wolf(Piece):
    def get_image(self):
        path = pathlib.Path().resolve()
        return f"{path}/version1/icons/wolf_transparent.png"
            
    def is_move_valid(self, gameboard, x_from :int, y_from :int, x_to :int, y_to :int) -> bool:
        if not is_capture_move(x_from, y_from, x_to, y_to):
            return game.is_connected(x_from, y_from, x_to, y_to)

        in_between_x = (x_from + x_to) // 2
        in_between_y = (y_from + y_to) // 2
        piece = gameboard[in_between_x][in_between_y]
        return type(piece) == Sheep
    