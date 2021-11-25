from cmu_112_graphics import *
from entities import *
from worldgen import *
from player import *
from game import *
from mobs import *
from crafting import *

#########################################################################
# NOTE: cmu_112_graphics file used is MODIFIED to include distinct left #
# and right mouse button presses (for break and place block mechanisms) #
#########################################################################

#####################e
# Menu Screen
#####################

def menuMode_redrawAll(app, canvas):
    canvas.create_text(app.width/2, 400, text='Minecraft 2D Lite', font="Arial 26")
    canvas.create_text(app.width/2, 500, text='Press any key to start the game')

def menuMode_keyPressed(app, event):
    app.mode = 'gameMode'

#####################
# Game Mode
#####################

# Movement
def gameMode_keyPressed(app, event):
    if event.key == "d": app.player.movePlayerRight(True)
    if event.key == "a": app.player.movePlayerLeft(True)
    if event.key == "w": app.player.jumpPlayer()
    if event.key == '1': app.player.switchTool(1)
    if event.key == '2': app.player.switchTool(2)
    if event.key == '3': app.player.switchTool(3)
    if event.key == '4': app.player.switchTool(4)
    if event.key == '5': app.player.switchTool(5)
    if event.key == 'e': app.mode = 'craftMode'

    # For testing purposes
    if event.key == 's': app.player.down()
    if event.key == 'Up': app.player.FLY()

def gameMode_keyReleased(app, event):
    if event.key == "d":
        app.player.movePlayerRight(False)
    if event.key == "a":
        app.player.movePlayerLeft(False)
    
def gameMode_leftMousePressed(app, event):
    x, y = event.x, event.y
    app.player.breakBlock(x, y)
    app.player.attackBlock(x, y)

def gameMode_rightMousePressed(app, event):
    x, y = event.x, event.y
    app.player.placeBlock(x, y)

def gameMode_mouseMoved(app, event):
    app.player.mouseX = event.x
    app.player.mouseY = event.y

def gameMode_timerFired(app):
    app.timerCount += 1
    app.player.changeY()
    app.player.changeX()

    mobGenerator(app)
    if app.timerCount % 10 == 0:
        generateNewChunk(app)

    for mob in app.mobs:
            mob.takeStep()
            mob.inflictDamage()

    if app.player.health <= 0:
        app.mode = 'deathScreen'
        
def gameMode_redrawAll(app, canvas):
    drawGrid(app, canvas)
    app.player.render(canvas)
    app.player.highlightBlock(canvas, app.player.mouseX, app.player.mouseY)
    drawMobs(app, canvas)

    canvas.create_text(400, 100, text=f"Selected Block = {app.player.selectedStack + 1}")
    for index in range(5):
        if app.player.inventory[index] != []:
            canvas.create_text(100, 110+index*20, text=f"Stack{index} = {app.player.inventory[index][0]}: {len(app.player.inventory[index])}")
        else:
            canvas.create_text(100, 110+index*20, text=f"Stack{index} = Empty")
    canvas.create_text(100, 250, text=f"Health: {app.player.health}")

    # canvas.create_text(400, 200, text=f"Inventory = {app.player.inventory}")
    # canvas.create_text(400, 150, text=f"On floor = {app.player.isOnFloor()}")
    # canvas.create_text(400, 250, text=f"dx, dy = {app.player.dx, app.player.dy}")


#####################
# Crafting
#####################
def craftMode_redrawAll(app, canvas):
    canvas.create_text(app.width/2, 100, text='Press "e" to exit inventory and return to game')
    drawInventory(app, canvas)

def craftMode_leftMousePressed(app, event):
    selectCell(app, event.x, event.y-150)
    moveItemHand(app)

def craftMode_keyPressed(app, event):
    app.mode = 'gameMode'

###############
# Death Screen
###############

def deathScreen_redrawAll(app, canvas):
    canvas.create_text(app.width/2, 100, text='You Died! Press r to respawn')

def deathScreen_keyPressed(app, event):
    if event.key == "r":
        appStarted(app)
        app.mode = 'gameMode'

###############
# Main App 
###############
def appStarted(app):
    app.mode = 'menuMode'
    app.timerCount = 0
    app.cols = 100
    app.rows = 100
    app.chunkRow = 100 # generate this much at one time
    app.chunkCol = 50
    app.grid = genChunk(app, app.rows, app.cols) # Initial chunk generation
    app.blockLen = 20
    app.player = Player(app, app.grid)
    app.scrollX = 0
    app.scrollY = 0
    app.timerDelay = 10 #10ms delay
    app.mobs = []
    app.breakBlock = True

    # Crafting
    app.craftMargin = 200
    app.craftSelect = (-1, -1)

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

runApp(width=1400, height=800)