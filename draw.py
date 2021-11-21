from cmu_112_graphics import *
from entities import *
from worldgen import *
from player import *
from game import *
from mobs import *

def appStarted(app):
    app.cols = 100
    app.rows = 100
    app.grid = genChunk(app, app.rows, app.cols)
    app.blockLen = 20
    app.player = Player(app, app.grid)
    app.scrollX = 0
    app.scrollY = 0
    app.timerDelay = 10
    app.mobs = [spawnBat(app, 100, 100)]
    app.breakBlock = True


# Movement
def keyPressed(app, event):
    if event.key == "d":
        app.player.movePlayerRight(True)
    if event.key == "a":
        app.player.movePlayerLeft(True)
    if event.key == "w":
        app.player.jumpPlayer()
    if event.key == 's':
        app.player.down()
    # For testing purposes
    if event.key == 'Up':
        app.player.FLY()

    if event.key == 'q':
        app.breakBlock = not app.breakBlock

def keyReleased(app, event):
    if event.key == "d":
        app.player.movePlayerRight(False)
    if event.key == "a":
        app.player.movePlayerLeft(False)
    
def mousePressed(app, event):
    x, y = event.x, event.y
    if app.breakBlock:
        app.player.breakBlock(x, y)
    else:
        app.player.placeBlock(x, y)
    

# def leftMousePressed(app, event):
#     x, y = event.x, event.y
#     print(f"{x, y}")

# def rightMousePressed(app, event):
#     x, y = event.x, event.y
#     print(f"{x, y}")

def timerFired(app):
    app.player.changeY()
    app.player.changeX()
    # app.player.gravity()
    for mob in app.mobs:
        mob.takeStep()

# TODO:
def drawMobs(app, canvas):
    for mob in app.mobs:
        mob.render(canvas)

# calculate what is needed to be draw on screen at a time,
# and then pass these row col parameters into the nested loops
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
    drawMobs(app, canvas)
    canvas.create_text(400, 100, text=f"Breaking Block = {app.breakBlock}")
    canvas.create_text(400, 200, text=f"ScrollY = {app.scrollY}")
    canvas.create_text(400, 150, text=f"On floor = {app.player.isOnFloor()}")
    canvas.create_text(400, 250, text=f"dx, dy = {app.player.dx, app.player.dy}")
runApp(width=1400, height=800)
