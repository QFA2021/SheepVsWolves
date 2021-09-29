import pyglet as pg
import game
from pyglet.window import mouse
from pyglet import image
from pyglet.gl import *
import enum
import pieces
import abc

# TODOS:
# - double jump
# - signal that game is over (restart)
# - show whos move it is
# - sheep counter
# - quantum mechanics
#   - superposition

window_width = 800
grid_margin = 100
field_radius = 30
field_color = (255, 0, 24)
selected_color = (24, 0, 255)
teleportation_active_color = (201, 13, 155)
teleportation_inactive_color = (30, 0, 30)

grid_margin = 100
window_width = 800
center_margin = window_width / 2 - 3 * grid_margin

icon_size = 80

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
        menu = pg.text.Label("MENU", font_name='Times New Roman', font_size=50, x=window.width // 2, y=window.height,
                             anchor_x='center', anchor_y='top')
        menu.draw()
        # start game
        start_rectangle = pg.shapes.BorderedRectangle(window.width // 2, window.height // 2,
                                                      window.width // 2, window.height // 4,
                                                      border=20, color=(255, 0, 24), border_color=(0, 0, 255))
        start_rectangle.anchor_position = (window.width // 4, 0)
        start_rectangle.opacity = 160
        start_rectangle.draw()
        start_text = pg.text.Label("Start Game", font_name='Times New Roman', font_size=30,
                                   x=window.width // 2, y=window.height // 2 + 15 * window.height // 100,
                                   anchor_x='center', anchor_y='top')
        start_text.draw()
        # start quantum game
        q_start_rectangle = pg.shapes.BorderedRectangle(window.width // 2, window.height // 4,
                                                        window.width // 2, window.height // 4,
                                                        border=20, color=(255, 0, 24), border_color=(0, 0, 255))
        q_start_rectangle.anchor_position = (window.width // 4, 0)
        q_start_rectangle.opacity = 160
        q_start_rectangle.draw()
        q_start_text = pg.text.Label("Start Quantum Game", font_name='Times New Roman', font_size=30,
                                     x=window.width // 2, y=window.height // 4 + 15 * window.height // 100,
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

    def on_draw(self):
        window.clear()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        gb = self.current_game.gameboard

        # background
        path = pieces.get_path("icons/background.png")
        pic = pg.image.load(path)
        pic.blit(0, 0)

        # draw grid
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

        # draw circles
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
        batch = pg.graphics.Batch()

        # draw sheep and wolfs
        sprites = []
        for row in range(7):
            for column in range(7):
                pos = self.ind_to_cord(row, column)
                entry = gb[row][column]
                if entry is not None:
                    image = entry.get_image()
                    image.anchor_x = image.width // 2
                    image.anchor_y = image.height // 2
                    scale_factor = icon_size / image.width
                    sprite = pg.sprite.Sprite(image, pos[0], pos[1], batch=batch)
                    sprite.scale = scale_factor
                    sprites.append(sprite)

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

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            global indices_leftclick
            indices_leftclick = self.get_indices(x, y)
            print(indices_leftclick)
            if self.current_game.is_clickable(indices_leftclick[0], indices_leftclick[1]):
                self.current_game.click_action(indices_leftclick[0], indices_leftclick[1])

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


screen = MenuScreen()

def to_game_screen(mode: game.GameMode):
    global screen
    game_screen = GameScreen()
    game_screen.current_game = game.Game(mode)
    screen = game_screen

@window.event
def on_draw():
    screen.on_draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    screen.on_mouse_press(x, y, button, modifiers)

@window.event
def on_close():
    window.close()


if __name__ == '__main__': 
     pg.app.run()