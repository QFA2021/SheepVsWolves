# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 09:16:36 2021

@author: Elias, Jan, Martin
"""
import random
from pieces import Sheep, Wolf
import enum
import pieces


class GameMode(enum.Enum):
    NORMAL = 1
    QUANTUM = 2


# The state indicates which action is next to be performed
class TurnState(enum.Enum):
    SELECTING = 1
    MOVING = 2

    # selecting a swapping partner as a wolf after moving onto the teleportation field
    SELECTING_TP_PARTNER = 3

    # placing the other entangled sheep into the stable when one of them gets there
    PLACE_IN_STABLE = 4

    # Tracks whether the game is over. This is the case if ether there are
    # less than 9 sheep left or the stable is full
    OVER = 9

    def requires_selection(self):
        return self == self.MOVING or self == self.SELECTING_TP_PARTNER \
               or self == self.PLACE_IN_STABLE


class Game:
    gameboard = []

    def __init__(self, mode):
        self.sheep_in_stable = 0
        self.sheep_left = 20

        self.mode = mode

        # Indicating whether its the sheep players or the wolfs turn
        self.sheeps_turn = True
        # Currently in the first phase of a turn; selecting a piece to move
        self.state = TurnState.SELECTING

        self.selected_x = -1
        self.selected_y = -1

        self.teleportation_cooldown = 0
        self.teleportation_just_activated = False

        self.entanglement_id_to_remove = -1

        self.init_gameboard()

    def init_gameboard(self):
        self.gameboard = [[None for x in range(7)] for y in range(7)]

        # add sheep
        sheep = []
        for y in range(4):
            for x in range(7):
                if not is_outside(x, y):
                    s = Sheep()
                    sheep.append(s)
                    self.gameboard[x][y] = s

        # add wolfs
        self.gameboard[2][4] = Wolf()
        self.gameboard[4][4] = Wolf()

        if self.mode == GameMode.QUANTUM:
            self.init_random_entanglement(sheep)

    def init_random_entanglement(self, sheep):
        for i in range(3):
            (sheep1, sheep2) = random.sample(sheep, 2)
            sheep1.entanglement_id = i
            sheep2.entanglement_id = i
            sheep.remove(sheep1)
            sheep.remove(sheep2)

    def is_clickable(self, x: int, y: int) -> bool:
        # SELECTING
        if self.state == TurnState.SELECTING:
            if self.is_empty(x, y):
                return False

            piece = self.gameboard[x][y]
            if self.sheeps_turn:
                return type(piece) == pieces.Sheep
            else:
                return type(piece) == pieces.Wolf

        # MOVING
        elif self.state == TurnState.MOVING:
            selected_piece = self.get_selected_piece()
            if not self.is_empty(x, y):
                # Reselection
                piece = self.get_selected_piece()
                if isinstance(piece, type(self.gameboard[x][y])):
                    self.state = TurnState.SELECTING
                    return True
                else:
                    return False

            valid = selected_piece.is_move_valid(self.gameboard, self.selected_x, self.selected_y, x, y)
            print(f"is move to {x},{y} valid {valid}")
            return valid

        # TELEPORTATION
        elif self.state == TurnState.SELECTING_TP_PARTNER:
            piece = self.gameboard[x][y]
            return type(piece) == Sheep and not is_in_stable(x, y)

        # ENTANGLEMENT
        elif self.state == TurnState.PLACE_IN_STABLE:
            return is_in_stable(x, y) and self.is_empty(x, y)

    def get_selected_piece(self) -> pieces.Piece:
        return self.gameboard[self.selected_x][self.selected_y]

    # Performs the action according to the current game state
    # Attention:    Before calling this method, check whether this point is 
    #               clickable!
    def click_action(self, x: int, y: int):

        # SELECTING
        if self.state == TurnState.SELECTING:
            self.selected_x = x
            self.selected_y = y
            print(f"{x},{y} selected")

        # MOVING
        elif self.state == TurnState.MOVING:
            print(f"moving to {x},{y}")
            piece = self.get_selected_piece()

            if type(piece) is pieces.Sheep:
                self.move_sheep(piece, x, y)
            elif type(piece) is pieces.Wolf:
                self.move_wolf(piece, x, y)

        # TELEPORTATION
        elif self.state == TurnState.SELECTING_TP_PARTNER:
            print(f"{x},{y} selected for swapping")
            self.swap(x, y, self.selected_x, self.selected_y)

        # ENTANGLEMENT
        elif self.state == TurnState.PLACE_IN_STABLE:
            entangled_sheep = self.get_selected_piece()
            self.move_sheep(entangled_sheep, x, y)

        self.update_state()

    def deselect_piece(self):
        print('deselect')
        self.state = TurnState.selecting

    def update_state(self):
        # SELECTING
        if self.state == TurnState.SELECTING:
            self.state = TurnState.MOVING

        # MOVING
        elif self.state == TurnState.MOVING:
            self.state = TurnState.SELECTING

            if self.teleportation_just_activated:
                self.teleportation_just_activated = False
                self.state = TurnState.SELECTING_TP_PARTNER

            elif self.entanglement_id_to_remove != -1:
                self.state = TurnState.PLACE_IN_STABLE

            else:
                self.sheeps_turn = not self.sheeps_turn

        # TELEPORTATION
        elif self.state == TurnState.SELECTING_TP_PARTNER:
            self.state = TurnState.SELECTING
            self.sheeps_turn = True
            self.teleportation_cooldown = 3

        # ENTANGLEMENT
        elif self.state == TurnState.PLACE_IN_STABLE:
            self.remove_entanglement()
            self.state = TurnState.SELECTING
            self.sheeps_turn = False

        self.check_win()
        self.manage_selection()

    def manage_selection(self):
        if not self.state.requires_selection():
            self.selected_x = -1
            self.selected_y = -1

    def check_win(self):
        if self.sheep_in_stable >= 9:
            self.state = TurnState.OVER
            print("Sheep won!")

        if self.sheep_left < 9:
            self.state = TurnState.OVER
            print("Wolf won!")

    def swap(self, x1, y1, x2, y2):
        temp = self.gameboard[x1][y1]
        self.gameboard[x1][y1] = self.gameboard[x2][y2]
        self.gameboard[x2][y2] = temp

    def move_sheep(self, sheep: pieces.Sheep, x: int, y: int):
        self.move_piece_simple(sheep, x, y)

        if is_in_stable(x, y) and not is_in_stable(self.selected_x, self.selected_y):
            self.sheep_in_stable += 1

            # entangled sheep
            id = sheep.entanglement_id
            if id != -1:
                pos = self.find_entangled_sheep(id)
                if pos != (-1, -1):
                    self.selected_x = pos[0]
                    self.selected_y = pos[1]
                    self.entanglement_id_to_remove = id

        print(f"sheep moved to {x},{y}")

    def move_wolf(self, wolf: pieces.Wolf, x: int, y: int):
        self.move_piece_simple(wolf, x, y)

        capture = False
        if abs(x - self.selected_x) == 2 or abs(y - self.selected_y) == 2:
            capture = True

        if capture:
            # A capture move was made, so a sheep has been captured
            in_between_x = (x + self.selected_x) // 2
            in_between_y = (y + self.selected_y) // 2

            self.capture_sheep(in_between_x, in_between_y)

        # Teleportation
        if self.mode == GameMode.QUANTUM:
            if self.is_teleportation(x, y) and self.teleportation_cooldown == 0:
                self.teleportation_just_activated = True
                self.selected_x = x
                self.selected_y = y
                print("Teleportation activated!")

            if self.teleportation_cooldown > 0:
                self.teleportation_cooldown -= 1

        print(f"wolf moved to {x},{y}")

    def capture_sheep(self, x, y):
        sheep = self.gameboard[x][y]
        self.gameboard[x][y] = None
        self.sheep_left -= 1

        # deal with entanglement
        id = sheep.entanglement_id
        if id != -1:
            entangled = self.find_entangled_sheep(id)
            if entangled != (-1, -1):
                self.capture_sheep(entangled[0], entangled[1])

        # Sheep in the stable has been eaten
        if is_in_stable(x, y):
            self.sheep_in_stable -= 1

    def find_entangled_sheep(self, id) -> (int, int):
        for x in range(7):
            for y in range(7):
                if is_in_stable(x, y):
                    continue
                piece = self.gameboard[x][y]
                if type(piece) is Sheep:
                    if piece.entanglement_id is id:
                        return (x, y)

        return (-1, -1)

    def remove_entanglement(self):
        print("removing entanglement")
        if self.entanglement_id_to_remove == -1:
            return

        for x in range(7):
            for y in range(7):
                piece = self.gameboard[x][y]
                if type(piece) is pieces.Sheep:
                    if piece.entanglement_id == self.entanglement_id_to_remove:
                        self.gameboard[x][y].entanglement_id = -1

    def move_piece_simple(self, piece: pieces.Piece, x: int, y: int):
        self.gameboard[self.selected_x][self.selected_y] = None
        self.gameboard[x][y] = piece

    def is_empty(self, x, y) -> bool:
        if not is_outside(x, y):
            return self.gameboard[x][y] is None
        return False

    def is_teleportation(self, x: int, y: int) -> bool:
        if self.mode == GameMode.NORMAL:
            return False
        return x == 3 and y == 3


def is_in_stable(x: int, y: int) -> bool:
    if y < 4: return False
    if x < 2 or x > 4: return False
    return True


def is_outside(x: int, y: int) -> bool:
    if (x < 0 or x > 6): return True
    if (y < 0 or y > 6): return True
    if y < 2 or y > 4:
        if x < 2 or x > 4:
            return True
    return False


# whether two points are connected on the gameboard via the grid
def is_connected(x1: int, y1: int, x2: int, y2: int) -> bool:
    if x1 == x2 and y1 == y2:
        return False

    if (x1 - x2) ** 2 + (y1 - y2) ** 2 > 2:
        return False

    if is_outside(x1, y1) or is_outside(x2, y2):
        return False

    return is_connected_straight(x1, y1, x2, y2) or is_connected_diagonally(x1, y1, x2, y2)


def is_connected_straight(x1: int, y1: int, x2: int, y2: int) -> bool:
    return (abs(x1 - x2) == 1) != (abs(y1 - y2) == 1)


def is_connected_diagonally(x1: int, y1: int, x2: int, y2: int) -> bool:
    return (x1 - y1) % 2 == 0 and (x2 - y2) % 2 == 0
