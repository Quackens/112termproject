#######################################################################
# This file contains functions that changes the gameplay in real time
#######################################################################

from entities import *
from player import *
from mobs import *
from worldgen import *
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
        batRow, batCol = GetBounds.RowCol(app, x, y)
        if isinstance(app.grid[batRow][batCol], AirBlock):
            app.mobs.append(spawnBat(app, x, y))

# Updates app.player.currChunk as it moves
def updatePlayerChunk(app):
    pass

# Determines if player has strayed far enough to append a new chunk
def generateNewChunk(app):
    (px0, py0, px1, py1) = app.player.getPlayerBounds()
    playerRow, playerCol = GetBounds.RowCol(app, px0 + app.blockLen/2, py0 + app.blockLen)
    # print(abs(playerCol - app.cols)) #bug found: playerrow col not updating
    if abs(playerCol - app.cols) < 40:
        appendChunks(app)

def appendChunks(app):
    colOffset = app.cols # Takes into account the top level terrain generation
    newChunk = genChunk(app, app.chunkRow, app.chunkCol, colOffset)
    for i in range(len(newChunk)):
        app.grid[i].extend(newChunk[i])
    app.player.currChunk = app.grid
    app.cols += app.chunkCol

# TODO: save game mechanic?
    # Convert block information, inventory, player and mob posiiton into string using repr
    # then store string into a csv file
    
def drawPlayerHealth(app, canvas):
    # One heart (red square) for every 100 health
    hearts = app.player.health // 100
    heartMargin = 50
    for i in range(hearts):
        canvas.create_rectangle(heartMargin + i*(10), 40, heartMargin + 10 + i*(10), 50, fill="Red")
    canvas.create_text(10, 40, text="Health:", anchor = 'nw')

def drawToolBar(app, canvas):
    for i in range(5):
        margin = 100
        size = 100
        if i == app.player.selectedStack:
            canvas.create_rectangle(50, margin + i*size, 150, margin + (i+1)*size, outline="Red", width=5)
        else:
            canvas.create_rectangle(50, margin + i*size, 150, margin + (i+1)*size, width=2)

        cx, cy = 100, (margin + i*size + margin + (i+1)*size) / 2
        if app.player.inventory[i] != []:
            canvas.create_text(cx, cy, text=f"{app.player.inventory[i][0]}: {len(app.player.inventory[i])}")
        else:
            canvas.create_text(cx, cy, text=f"")
    


 



