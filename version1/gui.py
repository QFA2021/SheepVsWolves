import pyglet as pg
import game
from pyglet.window import mouse
from pyglet import image
from pyglet.gl import *
import pathlib
import pieces
from pyglet import font


def get_path_fonts(file:  str) -> str:
    path = str(pathlib.Path().resolve())
    if not path.__contains__("fonts"):
        path += "/fonts"
    return f"{path}/{file}"


font_path = get_path_fonts("Quantum.otf")
font.add_file(font_path)
q_font = font.load('Quantum', 25)


window_width = 800
grid_margin = 100
field_radius = 30
field_color = (255, 0, 24)
selected_color = (24, 0, 255)
teleportation_active_color = (201, 13, 155)
teleportation_inactive_color = (30, 0, 30)
blue = (0,0,255)
red = (25,25,50)
grid_margin = 100
window_width = 800
center_margin = window_width/2 - 3*grid_margin


#making an intro screen
intro = pg.window.Window(window_width, window_width, visible=True)
#making game window
window = pg.window.Window(window_width, window_width, visible=False)


# Initialization stuff here
current_game = game.Game(game.GameMode.NORMAL)

@intro.event
def on_draw():
    intro.clear()
    menu = pg.text.Label("Wolves vs. Sheep", font_name = 'Quantum', font_size = 56, x = intro.width//2, y = intro.height,
                         anchor_x = 'center', anchor_y = 'top')
    menu.draw()
    #start game
    start_rectangle = pg.shapes.BorderedRectangle(intro.width//2,intro.height//2,
                                                  intro.width//2, intro.height//4,
                                                  border = 20, color = red, border_color = blue)
    start_rectangle.anchor_position = (intro.width//4, 0)
    start_rectangle.opacity = 160
    start_rectangle.draw()
    start_text = pg.text.Label("Start Game", font_name = 'Quantum', font_size = 22,
                               x = intro.width//2, y = intro.height//2 + 15*intro.height//100,
                               anchor_x = 'center', anchor_y = 'top')
    start_text.draw()
    #start quantum game
    q_start_rectangle = pg.shapes.BorderedRectangle(intro.width//2,intro.height//4-intro.width//12,
                                                  intro.width//2, intro.height//4,
                                                  border = 20, color = red, border_color = blue)
    q_start_rectangle.anchor_position = (intro.width//4, 0)
    q_start_rectangle.opacity = 160
    q_start_rectangle.draw()
    q_start_text = pg.text.Label("Start Quantum Game", font_name = 'Quantum', font_size = 22,
                               x = intro.width//2, y = intro.height//4 + 15*intro.height//100-intro.width//12,
                               anchor_x = 'center', anchor_y = 'top')
    q_start_text.draw()
    
@intro.event
def on_close():
    window.close()

@intro.event
def on_mouse_press(x,y,button,modifiers):
    global current_game

    if button == mouse.LEFT and x>intro.width//4 and x<3*intro.width//4 and y>intro.width//2 and y<3*intro.width//4:
        intro.close()
        window.set_visible()
    if button == mouse.LEFT and x>intro.width//4 and x<3*intro.width//4 and y>intro.width//4 and y<intro.width//2:
        intro.close()
        window.set_visible()
        current_game = game.Game(game.GameMode.QUANTUM)


# TODOS:
# - double jump
# - signal that game is over (restart)
# - show how move it is
# - sheep counter
# (- reselecting)
# - quantum mechanics
#   - teleportation
#   - entanglement
# (- mode selection)

@window.event
def on_draw():
    window.clear()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    gb = current_game.gameboard
    print('draw')
    #background
    path = pieces.get_path("icons/background.png")
    pic = image.load(path)
    pic.blit(0,0)
    
    # draw grid
    batch = pg.graphics.Batch()
    for row in range(7):
        for column in range(7):
            for offset_row in range(-1, 2):
                for offset_column in range(-1, 2):
                    row2 = row + offset_row
                    column2 = column + offset_column
                    if game.is_connected(column, row, column2, row2):
                        pos1 = ind_to_cord(row, column)
                        pos2 = ind_to_cord(row2, column2)
                        line = pg.shapes.Line(pos1[0], pos1[1],
                                              pos2[0], pos2[1],
                                              width=5,
                                              color = field_color,
                                              batch=batch)  
                    batch.draw()

    
    # draw circles
    batch = pg.graphics.Batch()
    for row in range(7):
        for column in range(7):
            if game.is_outside(column, row): continue
            x = column * grid_margin + center_margin
            y = row * grid_margin + center_margin
            
            
            # teleportation field
            if current_game.is_teleportation(column, 6 - row):
                color = teleportation_inactive_color
                if current_game.teleportation_cooldown == 0:
                    color = teleportation_active_color
                    
                circle = pg.shapes.Circle(x, y, field_radius + 5, 
                                          color=color, batch=batch)
                batch.draw()
            
            
            # mark selection
            color = field_color
            if current_game.selected_x == column and current_game.selected_y == 6 - row:
                color = selected_color
               
          
            
            circle = pg.shapes.Circle(x, y, field_radius, color=color, batch=batch)
            batch.draw()
    
    # draw sheep and wolfs
    for row in range(7):
        for column in range(7):
            pos = ind_to_cord(row, column)
            entry = gb[row][column]
            if entry is not None:
                pic = image.load(entry.get_image())
                pic.anchor_x = pic.width // 2
                pic.anchor_y = pic.height // 2
                pic.blit(pos[0], pos[1])

            # marking entanglement
            if type(entry) is pieces.Sheep:
                if entry.entanglement_id != -1:
                    id = entry.entanglement_id
                    x = pos[0] + 20
                    y = pos[1] + 20
                    label = pg.text.Label(str(id), font_size=18, x=x, y=y)
                    label.color = (255, 255, 0, 255)
                    label.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        global indices_leftclick
        indices_leftclick = get_indices(x, y)
        print(indices_leftclick)
        if current_game.is_clickable(indices_leftclick[0], indices_leftclick[1]):
            current_game.click_action(indices_leftclick[0], indices_leftclick[1])
        
        
def get_indices(x, y):
    (i,j) = (-1, -1)
    x = x - center_margin
    y = y - center_margin
    for a in range(7):
        for b in range(7):
            temp_dist = (x-grid_margin*a)**2 + (y-grid_margin*b)**2
            if temp_dist <= field_radius**2:
                (i,j) = (a,6-b)
    if game.is_outside(i,j):
        return (-1,-1)
    return (i,j)

def ind_to_cord(i,j):
    (i,j) = (i,6-j)
    return (center_margin+i*grid_margin, center_margin+j*grid_margin)

if __name__ == '__main__': 
     pg.app.run()