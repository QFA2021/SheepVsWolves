import pyglet as pgfrom game import Game import gamefield_radius = 20field_color = (250, 0, 0)grid_margin = 30window = pg.window.Window(800, 600, visible=False)# Initialization stuff herecurrent_game = game.Game()window.set_visible()# TODOS:# programmeticly draw the gameboard # for the concrete placement of the pieces get the images from the subclasses# on click pass it on the the gameBoard@window.eventdef on_draw():    window.clear()        gb = current_game.gameboard    batch = pg.graphics.Batch()        # draw the raw gameboard    for row in range(7):        for column in range(7):            if game.isOutside(column, row): continue                        x = column * grid_margin            y = row * grid_margin            circle = pg.shapes.Circle(x, y, field_radius, color=field_color, batch=batch)            batch.draw()if __name__ == '__main__':      pg.app.run()