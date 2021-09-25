import pyglet as pg
from game import Game 
import game
from pyglet.window import mouse
import numpy as np
from pyglet import image
import pieces
from pyglet.gl import *

field_radius = 30
field_color = (255, 0, 24)
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
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    gb = current_game.gameboard
    
    #background
    pic = image.load("icons/background.png")
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
            if game.isOutside(column, row): continue
            x = column * grid_margin
            y = row * grid_margin
            circle = pg.shapes.Circle(x+center_margin, y+center_margin, 
                                      field_radius, color=field_color, batch=batch)
            batch.draw()
    batch.draw()
    
    #draw sheep
    batch = pg.graphics.Batch()
    for row in range(7):
        for column in range(7):
            pos = ind_to_cord(row, column)
            entry = gb[row][column]
            if entry!=None:
                pic = image.load(entry.getImage())
                pic.anchor_x = pic.width // 2
                pic.anchor_y = pic.height // 2
                pic.blit(pos[0], pos[1])                



    
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