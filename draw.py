from cmu_112_graphics import *
from entities import *
from physics import *
from worldgen import *
from initialize import *
from player import *

def appStarted(app):
    app.cols = 50
    app.rows = 40
    app.grid = genChunk(app, app.rows, app.cols)
    app.blockLen = 20
    app.player = Player(app, app.grid)
    app.scrollX = 0
    app.scrollY = 0
    app.timerDelay = 10

# TODO: draw a grid of 'empty' and 'filled' grids
# TODO: draw grass blocks are green rectangles as floor
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
# TODO: Breaking and removing blocks
def mousePressed(app, event):
    x, y = event.x, event.y
    app.player.breakBlock(x, y)

def timerFired(app):
    app.player.gravity()

def drawGrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            app.grid[row][col].render(canvas)

def redrawAll(app, canvas):
    drawGrid(app, canvas)
    app.player.render(canvas)
    canvas.create_text(400, 100, text=f"ScrollX = {app.scrollX}")
    canvas.create_text(400, 200, text=f"ScrollY = {app.scrollY}")
    canvas.create_text(400, 150, text=f"On floor = {app.player.isOnFloor()}")

runApp(width=800, height=800)
