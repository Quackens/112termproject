from entities import *
from player import *
from mobs import *
import random
# TODO: implement some mob generating mechanic where mobs are 
#       spawned above and below ground relative to where player is
def spawnBat(app, x, y):
    return Bat(app, app.grid, x, y)

# Radius around player only has 5 mobs at any given time. 
def mobGenerator(app):
    radius = 30
    (px0, py0, px1, py1) = app.player.getPlayerBounds()
    playerRow, playerCol = GetBounds.RowCol(app, px0 + app.blockLen/2, py0 + app.blockLen/2)
    while len(app.mobs) < 5:
        row, col = playerRow + random.randint(-radius, radius) , playerCol + random.randint(-radius, radius)
        (x0, y0, x1, y1) = GetBounds.Cell(app, row, col)
        x = x0 + app.blockLen/2
        y = y0 + app.blockLen/2
        app.mobs.append(spawnBat(app, x, y))

# TODO: save game mechanic?
    # Convert block information, inventory, player and mob posiiton into string using repr
    # then store string into a csv file

def drawInventory(app, canvas):
    inventory = app.player.inventory
    toolbar = app.player.toolBar
    for i in range(5):
        pass
    



