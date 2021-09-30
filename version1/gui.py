import pyglet as pg
import game
from pyglet.window import mouse
from pyglet import image
from pyglet.gl import *
import pathlib
import pieces
from pyglet import font
import enum
import abc


# TODOS:
# - mute sound
# - how to play
# - stack dead sheep
# - scale images statically


def get_path_fonts(file: str) -> str:
    path = str(pathlib.Path().resolve())
    if not path.__contains__("version1"):
        path += "/version1"
    return f"{path}/{file}"


font_path = get_path_fonts("fonts/Quantum.otf")
font.add_file(font_path)
q_font = font.load('Quantum', 25)

window_width = 800
grid_margin = 100
field_radius = 30
field_color = (200, 0, 25)
selected_color = (24, 0, 255)
teleportation_active_color = (201, 13, 155)
teleportation_inactive_color = (30, 0, 30)
blue = (0, 0, 255)
red = (25, 25, 50)
grid_margin = 100
window_width = 800
center_margin = window_width / 2 - 3 * grid_margin

icon_size_sheep = 80
icon_size_wolf = 62

window = pg.window.Window(window_width, window_width, visible=True)


class Screen(abc.ABC):
    @abc.abstractmethod
    def on_draw(self):
        pass

    @abc.abstractmethod
    def on_mouse_press(self, x, y, button, modifiers):
        pass


# MENU_SCREEN
class MenuScreen(Screen):
    def on_draw(self):
        window.clear()
        menu = pg.text.Label("Wolves vs. Sheep", font_name='Quantum', font_size=56, x=window.width // 2,
                             y=window.height - window.height // 16,
                             anchor_x='center', anchor_y='top')
        menu.draw()

        # start game
        start_rectangle = pg.shapes.BorderedRectangle(window.width // 2, window.height // 2,
                                                      window.width // 2, window.height // 4,
                                                      border=20, color=red, border_color=blue)
        start_rectangle.anchor_position = (window.width // 4, 0)
        start_rectangle.opacity = 160
        start_rectangle.draw()
        start_text = pg.text.Label("Start Game", font_name='Quantum', font_size=22,
                                   x=window.width // 2, y=window.height // 2 + 15 * window.height // 100,
                                   anchor_x='center', anchor_y='top')
        start_text.draw()

        # start quantum game
        q_start_rectangle = pg.shapes.BorderedRectangle(window.width // 2, window.height // 4 - window.width // 12,
                                                        window.width // 2, window.height // 4,
                                                        border=20, color=red, border_color=blue)
        q_start_rectangle.anchor_position = (window.width // 4, 0)
        q_start_rectangle.opacity = 160
        q_start_rectangle.draw()
        q_start_text = pg.text.Label("Start Quantum Game", font_name='Quantum', font_size=22,
                                     x=window.width // 2,
                                     y=window.height // 4 + 15 * window.height // 100 - window.width // 12,
                                     anchor_x='center', anchor_y='top')
        q_start_text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Top Button
        if button == mouse.LEFT and x > window.width // 4 and x < 3 * window.width // 4 and y > window.width // 2 and y < 3 * window.width // 4:
            to_game_screen(game.GameMode.NORMAL)
        # Bottom Button
        if button == mouse.LEFT and x > window.width // 4 and x < 3 * window.width // 4 and y > window.width // 4 and y < window.width // 2:
            to_game_screen(game.GameMode.QUANTUM)


# GAME_SCREEN
class GameScreen(Screen):
    def __init__(self):
        self.current_game = None
        self.back_size = 60
        margin = 30
        self.back_pos = (margin, window_width - margin - self.back_size)

        self.restart_active = False
        self.restart_pos = (350, 370)
        self.restart_size = 100

        sheep = pieces.default_sheep_image
        sheep.anchor_x = sheep.width // 2
        sheep.anchor_y = sheep.height // 2
        self.sheep_sprite = pg.sprite.Sprite(sheep)
        scale_factor = icon_size_sheep / sheep.width
        self.sheep_sprite.scale = scale_factor

        wolf = pieces.default_wolf_image
        wolf.anchor_x = wolf.width // 2
        wolf.anchor_y = wolf.height // 2
        self.wolf_sprite = pg.sprite.Sprite(wolf)
        scale_factor = icon_size_wolf / wolf.width
        self.wolf_sprite.scale = scale_factor

    def on_draw(self):
        window.clear()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        gb = self.current_game.gameboard

        # sky
        s_path = pieces.get_path("icons/sky.jpg")
        s_pic = pg.image.load(s_path)
        s_scale_factor = window_width / s_pic.width
        s_sprite = pg.sprite.Sprite(s_pic, 0, window_width // 2)
        s_sprite.scale = s_scale_factor
        s_sprite.draw()
        # background
        path = pieces.get_path("icons/background4.jpg")
        pic = pg.image.load(path)
        b_scale_factor = 1.06 * window_width / pic.width
        b_sprite = pg.sprite.Sprite(pic, 0, 0)
        b_sprite.scale = b_scale_factor
        b_sprite.draw()

        self.draw_grid()
        self.draw_circles()
        self.draw_pieces()
        self.draw_info()
        self.draw_turn_indicator()

        batch = pg.graphics.Batch()
        # sheep left counter
        count_str = str(self.current_game.sheep_left) + str('x')
        sheep_counter = pg.text.Label(count_str,
                                      font_name='Times New Roman',
                                      font_size=36,
                                      x=4.7 * grid_margin + center_margin, y=0.2 * grid_margin + center_margin)
        image = pg.image.load(pieces.get_path("icons/sheep.png"))
        pos = self.ind_to_cord(5.4, 6.0)
        scale_factor = icon_size_sheep / image.width
        sprite = pg.sprite.Sprite(image, pos[0], pos[1], batch=batch)
        sprite.scale = scale_factor
        sheep_counter.draw()
        batch.draw()

        # back button
        image = pg.image.load(pieces.get_path("icons/arrow_left.png"))
        scale_factor = self.back_size / image.width
        sprite = pg.sprite.Sprite(image, self.back_pos[0], self.back_pos[1], batch=batch)
        sprite.scale = scale_factor
        batch.draw()

        # mute button
        imstr = "icons/volume_up.jpg"
        if self.current_game.Muted:
            imstr = "icons/volume_off.jpg"
        image = pg.image.load(pieces.get_path(imstr))
        scale_factor = 0.8* self.back_size / image.width
        sprite = pg.sprite.Sprite(image, self.back_pos[0]+6, self.back_pos[1]-60, batch=batch)
        sprite.scale = scale_factor
        batch.draw()

        self.draw_winner_overlay()

    def draw_winner_overlay(self):
        winner_sheep = self.current_game.check_win()
        if winner_sheep == 0: return

        icon_size = 200
        x = 150
        y = 4 * window_width / 5

        # Overlay
        height = 300
        rect = pg.shapes.Rectangle(x, y - height, width=500, height=height)
        rect.color = (0, 0, 20)
        rect.opacity = 230
        rect.draw()

        # Icon + Label
        image = pieces.default_wolf_image
        if winner_sheep == 1:
            image = pieces.default_sheep_image

        sprite = pg.sprite.Sprite(image, x=x + 100, y=y - 100)
        sprite.scale = icon_size / sprite.width
        sprite.draw()
        label = pg.text.Label("won!",
                              font_name='Quantum',
                              font_size=100,
                              x=x + icon_size - 20, y=y - 140, color=(255, 200, 0, 255))
        label.draw()

        # Restart
        image = pg.image.load(pieces.get_path("icons/retry.png"))
        sprite = pg.sprite.Sprite(image, x=self.restart_pos[0], y=self.restart_pos[1])
        sprite.scale = 0.3
        sprite.draw()

        self.restart_active = True

    def draw_info(self):
        info = self.current_game.info
        if info == "": return

        x = 130
        y = window_width - 43
        width = 420

        # Info for entanglement
        if len(info) > 40:
            width = 615

        rect = pg.shapes.Rectangle(x, y - 18, width=width, height=44)
        rect.color = (0, 0, 20)
        rect.opacity = 200
        rect.draw()

        label = pg.text.Label(info,
                              font_name='Times New Roman',
                              font_size=20,
                              x=x+10, y=y)
        label.draw()

    def draw_turn_indicator(self):
        size = 400
        alpha = 0

        sheep = pieces.default_sheep_image
        sprite = pg.sprite.Sprite(sheep, x=50, y=100)
        sprite.scale = size / sheep.width
        sprite.rotation = 20
        if not self.current_game.sheeps_turn:
            sprite.opacity = alpha
        sprite.draw()

        wolf = pieces.default_wolf_image
        sprite = pg.sprite.Sprite(wolf, x=50, y=100)
        sprite.scale = (size / wolf.width) * 0.8
        sprite.rotation = 20
        if self.current_game.sheeps_turn:
            sprite.opacity = alpha
        sprite.draw()

    def draw_grid(self):
        batch = pg.graphics.Batch()
        lines = []
        for row in range(7):
            for column in range(7):
                for offset_row in range(-1, 2):
                    for offset_column in range(-1, 2):
                        row2 = row + offset_row
                        column2 = column + offset_column
                        if game.is_connected(column, row, column2, row2):
                            pos1 = self.ind_to_cord(row, column)
                            pos2 = self.ind_to_cord(row2, column2)
                            line = pg.shapes.Line(pos1[0], pos1[1],
                                                  pos2[0], pos2[1],
                                                  width=5,
                                                  color=field_color,
                                                  batch=batch)
                            lines.append(line)
        batch.draw()

    def draw_circles(self):
        batch = pg.graphics.Batch()
        circles = []

        for row in range(7):
            for column in range(7):
                if game.is_outside(column, row): continue
                x = column * grid_margin + center_margin
                y = row * grid_margin + center_margin

                # teleportation field
                if self.current_game.is_teleportation(column, 6 - row):
                    color = teleportation_inactive_color
                    if self.current_game.teleportation_cooldown == 0:
                        color = teleportation_active_color

                    circle = pg.shapes.Circle(x, y, field_radius + 5,
                                              color=color, batch=batch)
                    circles.append(circle)

                # mark selection
                color = field_color
                if self.current_game.selected_x == column and self.current_game.selected_y == 6 - row:
                    color = selected_color

                circle = pg.shapes.Circle(x, y, field_radius, color=color, batch=batch)
                circles.append(circle)

        batch.draw()

    def draw_pieces(self):
        batch = pg.graphics.Batch()
        sprites = []
        gb = self.current_game.gameboard

        for row in range(7):
            for column in range(7):
                pos = self.ind_to_cord(row, column)
                entry = gb[row][column]
                if entry is not None:
                    offset = 3
                    sprite = self.wolf_sprite
                    if type(entry) == pieces.Sheep:
                        offset = 0
                        sprite = self.sheep_sprite

                    sprite.x = pos[0] - offset
                    sprite.y = pos[1]
                    sprite.draw()

                # marking entanglement
                if type(entry) is pieces.Sheep:
                    if entry.entanglement_id != -1:
                        id = entry.entanglement_id
                        x = pos[0] + 20
                        y = pos[1] + 20
                        label = pg.text.Label(str(id), font_size=18, x=x, y=y)
                        label.color = (255, 255, 0, 255)
                        label.draw()
        batch.draw()

        #sheep left counter
        count_str = str(self.current_game.sheep_left)+str('x')
        sheep_counter = pg.text.Label(count_str,
                        font_name='Times New Roman',
                        font_size=36,
                        x=4.7 * grid_margin + center_margin, y=0.2* grid_margin + center_margin)
        image = pg.image.load(pieces.get_path("icons/sheep.png"))
        pos = self.ind_to_cord(5.4, 6.0)
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        scale_factor = icon_size_sheep / image.width
        sprite = pg.sprite.Sprite(image, pos[0], pos[1], batch=batch)
        sprite.scale = scale_factor
        sprites.append(sprite)
        sheep_counter.draw()


    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            global indices_leftclick
            indices_leftclick = self.get_indices(x, y)
            print(indices_leftclick)
            if self.current_game.is_clickable(indices_leftclick[0], indices_leftclick[1]):
                self.current_game.click_action(indices_leftclick[0], indices_leftclick[1])
            # Back Button
            if self.back_pos[0] <= x <= self.back_pos[0] + self.back_size \
                    and self.back_pos[1] <= y <= self.back_pos[1] + self.back_size:
                to_menu_screen()
            # Mute Button
            if self.back_pos[0] <= x <= self.back_pos[0] + self.back_size \
                    and self.back_pos[1]-50 <= y <= self.back_pos[1] + self.back_size -50:
                self.current_game.mute_music()

            # Restart Button
            if self.restart_active:
                if self.restart_pos[0] <= x <= self.restart_pos[0] + self.restart_size \
                        and self.restart_pos[1] <= y <= self.restart_pos[1] + self.restart_size:
                    print("Restart")
                    self.restart_active = False
                    self.current_game = game.Game(self.current_game.mode)

    def get_indices(self, x, y):
        (i, j) = (-1, -1)
        x = x - center_margin
        y = y - center_margin
        for a in range(7):
            for b in range(7):
                temp_dist = (x - grid_margin * a) ** 2 + (y - grid_margin * b) ** 2
                if temp_dist <= field_radius ** 2:
                    (i, j) = (a, 6 - b)
        if game.is_outside(i, j):
            return (-1, -1)
        return (i, j)

    def ind_to_cord(self, i, j):
        (i, j) = (i, 6 - j)
        return (center_margin + i * grid_margin, center_margin + j * grid_margin)


menu_screen = MenuScreen()
screen = menu_screen


def to_game_screen(mode: game.GameMode):
    global screen
    game_screen = GameScreen()
    game_screen.current_game = game.Game(mode)
    screen = game_screen


def to_menu_screen():
    global screen
    screen = menu_screen


@window.event
def on_draw():
    screen.on_draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    screen.on_mouse_press(x, y, button, modifiers)


@window.event
def on_close():
    window.close()
    game.Music.pause()


if __name__ == '__main__':
    pg.app.run()
