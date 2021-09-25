import pyglet as pg
from game import Game 
import game
from pyglet.window import mouse
import numpy as np
from pyglet import image

field_radius = 30
field_color = (250, 0, 0)
grid_margin = 100
window_width = 800
center_margin = window_width/2 - 3*grid_margin


window = pg.window.Window(window_width, window_width, visible=False)

# Initialization stuff here
current_game = game.Game()

window.set_visible()

# TODOS:
# programmeticly draw the gameboard 
# for the concrete placement of the pieces get the images from the subclasses

# on click pass it on the the gameBoard



@window.event
def on_draw():
    window.clear()
    
    gb = current_game.gameboard
    batch = pg.graphics.Batch()
    
    # draw circles
    for row in range(7):
        for column in range(7):
            if game.isOutside(column, row): continue
            x = column * grid_margin
            y = row * grid_margin
            circle = pg.shapes.Circle(x+center_margin, y+center_margin, field_radius, color=field_color, batch=batch)
            batch.draw()
    batch.draw()
    
    pic = image.load('icons/sheep.png')
    pic.width = 30
    pic.height = 30
    pic.anchor_x = pic.width // 2
    pic.anchor_y = pic.height // 2
    pic.blit(x, y)
    
    for row in range(7):
        for column in range(7):
            #draw horizontal lines
            pos = ind_to_cord(row,column)
            if not (game.isOutside(row+1,column) or game.isOutside(row, column)):
                line = pg.shapes.Line(pos[0]+field_radius,
                                      pos[1],
                                      pos[0]+grid_margin-field_radius,
                                      pos[1],
                                      width=5,
                                      batch=batch)
                batch.draw()
            #draw vertical lines
            if not (game.isOutside(row,column-1) or game.isOutside(row, column)):
                line = pg.shapes.Line(pos[0],
                                      pos[1]+field_radius,
                                      pos[0],
                                      pos[1]+grid_margin-field_radius,
                                      width=5,
                                      batch=batch)
                batch.draw()
            batch.draw()
    
    #TODO abstand schraege striche variable
    for (i,j) in ((1,3), (3,1), (3,3), (5,3), (3,5)):
        pos = ind_to_cord(i,j)
        fr = np.sqrt(1/2)*field_radius
        line1 = pg.shapes.Line(pos[0]+fr,
                               pos[1]+fr,
                               pos[0]+(grid_margin-fr),
                               pos[1]+(grid_margin-fr),
                               width=5,
                               batch=batch)
        line2 = pg.shapes.Line(pos[0]-fr,
                               pos[1]+fr,
                               pos[0]-(grid_margin-fr),
                               pos[1]+(grid_margin-fr),
                               width=5,
                               batch=batch)
        line3 = pg.shapes.Line(pos[0]-fr,
                               pos[1]-fr,
                               pos[0]-(grid_margin-fr),
                               pos[1]-(grid_margin-fr),
                               width=5,
                               batch=batch)
        line4 = pg.shapes.Line(pos[0]+fr,
                               pos[1]-fr,
                               pos[0]+(grid_margin-fr),
                               pos[1]-(grid_margin-fr),
                               width=5,
                               batch=batch)
        batch.draw()
    batch.draw()
    
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print(get_indices(x, y))
        # game.mark_field
        
def get_indices(x, y):
    (i,j) = (-1, -1)
    x = x - center_margin
    y = y - center_margin
    for a in range(7):
        for b in range(7):
            temp_dist = (x-grid_margin*a)**2 + (y-grid_margin*b)**2
            if temp_dist <= field_radius**2:
                (i,j) = (a,6-b)
    if game.isOutside(i,j):
        return (-1,-1)
    return (i,j)

def ind_to_cord(i,j):
    (i,j) = (i,6-j)
    return (center_margin+i*grid_margin, center_margin+j*grid_margin)

if __name__ == '__main__': 
     pg.app.run()

