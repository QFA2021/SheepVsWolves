# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 09:16:36 2021

@author: Elias, Jan, Martin
"""

import pyglet as pg
from pyglet.window import key

window = pg.window.Window(visible=False)
# ... perform some additional initialisation
window.set_visible()

label = pg.text.Label('Welcome to Hnefatafl!',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.UP:
        label.font_size += 10
    elif symbol == key.DOWN:
        label.font_size -= 10

@window.event
def on_draw():
    window.clear()
    label.draw()
    
pg.app.run()