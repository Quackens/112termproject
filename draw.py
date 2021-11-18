from cmu_112_graphics import *
from entities import *
from physics import *
from worldgen import *
from player import *

def appStarted(app):
    app.cols = 100
    app.rows = 100
    app.grid = genChunk(app, app.rows, app.cols)
    app.blockLen = 20
    app.player = Player(app, app.grid)
    app.scrollX = 0
    app.scrollY = 0
    app.timerDelay = 10

# Movement
def keyPressed(app, event):
    if event.key == "d":
        app.player.movePlayerRight()
    if event.key == "a":
        app.player.movePlayerLeft()
    if event.key == "w":
        app.player.jumpPlayer()
    if event.key == 's':
        app.player.down()
    # For testing purposes
    if event.key == 'Up':
        app.player.FLY()

def mousePressed(app, event):
    x, y = event.x, event.y
    app.player.breakBlock(x, y)

def timerFired(app):
    app.player.gravity()

# calculate what is needed to be draw on screen at a time, and then pass these row col parameters into the nested loops
def drawGrid(app, canvas):
    renderWidth = app.width // app.blockLen
    renderHeight = app.height // app.blockLen
    x0, y0, x1, y1 = app.player.getPlayerBounds()
    (row, col) = GetBounds.RowCol(app, x0, y0)
    renderR0, renderR1 = row - renderHeight, row + renderHeight
    renderC0, renderC1 = col - renderWidth, col + renderWidth

    for row in range(renderR0, renderR1):
        for col in range(renderC0, renderC1):
            if 0 <= row < app.rows and 0 <= col < app.cols:
                app.grid[row][col].render(canvas)

def redrawAll(app, canvas):
    drawGrid(app, canvas)
    app.player.render(canvas)
    canvas.create_text(400, 100, text=f"ScrollX = {app.scrollX}")
    canvas.create_text(400, 200, text=f"ScrollY = {app.scrollY}")
    canvas.create_text(400, 150, text=f"On floor = {app.player.isOnFloor()}")

runApp(width=1400, height=800)
