import copy
from entities import *

# Obtained from course notes, slightly modified
def getCellBounds(app, row, col):
    rows, cols = 4, 9
    gridWidth  = app.width - 2*app.craftMargin
    gridHeight = app.height - 2*app.craftMargin
    cellWidth = gridWidth / cols
    cellHeight = gridHeight / rows
    x0 = app.craftMargin + col * cellWidth
    x1 = app.craftMargin + (col+1) * cellWidth
    y0 = app.craftMargin + row * cellHeight
    y1 = app.craftMargin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

# Obtained from course notes, modified
def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.craftMargin <= x <= app.width-app.craftMargin) and
            (app.craftMargin <= y <= app.height-app.craftMargin))

# Returns if the click is in the craft menu (including the item grid)
def pointInCraft(app, x, y):
    cellWidth  = (app.width - 2*app.craftMargin) / 9
    cellHeight = (app.height - 2*app.craftMargin) / 4
    leftMargin = app.craftMargin
    topMargin = 20
    return (((leftMargin <= x <= leftMargin+3*cellWidth) and 
            (topMargin <= y <= topMargin+3*cellHeight)) or
            ((leftMargin+cellWidth*5 <= x <= leftMargin+cellWidth*6) and 
            (topMargin+cellHeight*1 <= y <= topMargin+cellHeight*2)))

# Obtained from course notes, modified
def getCell(app, x, y):
    rows, cols = 4, 9
    if (not pointInGrid(app, x, y)):
        if pointInCraft(app, x, y+150):
            craftWidth  = (app.width - 2*app.craftMargin) / 9
            craftHeight = (app.height - 2*app.craftMargin) / 4
            leftMargin = app.craftMargin
            topMargin = 20
            craftRow = int((y+150 - topMargin) / craftHeight)
            craftCol = int((x - leftMargin) / craftWidth)
            if leftMargin+craftWidth*5 <= x <= leftMargin+craftWidth*6:
                craftRow, craftCol = 4, 4 #Special case
            return (craftRow + 999, craftCol + 999) # extra 999 signifies crafting row
        else:
            return (-1, -1)

    gridWidth  = app.width - 2*app.craftMargin
    gridHeight = app.height - 2*app.craftMargin
    cellWidth  = gridWidth / cols
    cellHeight = gridHeight / rows
    row = int((y - app.craftMargin) / cellHeight)
    col = int((x - app.craftMargin) / cellWidth)
    return (row, col)

def selectCell(app, x, y):
    row, col = getCell(app, x, y)
    app.craftSelect = (row, col)

# Moves the selected item into your hand
def moveItemHand(app):
    row, col = app.craftSelect
    index = InvToList(row, col)
    # If player is holding nothing, put inentory items to player hand
    if app.player.inventoryHold == []:
        app.player.inventoryHold = copy.copy(app.player.inventory[index])
        app.player.inventory[index] = []
    # If player is holding something, switch hand with inventory slot
    else:
        # If inventory has nothing, place it in there
        if app.player.inventory[index] == []:
            app.player.inventory[index] = copy.copy(app.player.inventoryHold)
            app.player.inventoryHold = []
        
        # If inventory slot contains same type of item in hand, append
        elif type(app.player.inventory[index][0]) == type(app.player.inventoryHold[0]):
            app.player.inventory[index].extend(copy.copy(app.player.inventoryHold))
            app.player.inventoryHold = []

        # If inventory slot already has something, swap
        else:
            temp = copy.copy(app.player.inventory[index])
            app.player.inventory[index] = copy.copy(app.player.inventoryHold)
            app.player.inventoryHold = temp

# Moves selected item into crafting menu to and from hand
def moveItemCraft(app):
    row, col = app.craftSelect[0] % 999, app.craftSelect[1] % 999
    # Note: index 9 is the crafted item slot
    index = craftToList(row, col)
        # Hand must be empty to grab from crafting
    if index == 9 and app.player.inventoryHold == []:
        app.player.inventoryHold = copy.copy(app.player.craftGrid[index])
        app.player.craftGrid[index] = []
        depleteCraft(app)
    else:
        # If holding nothing, switch from craft menu to hand
        if app.player.inventoryHold == []:
            app.player.inventoryHold = copy.copy(app.player.craftGrid[index])
            app.player.craftGrid[index] = []
        # If holding something, switch hand with crafting grid slot
        else:
            if app.player.craftGrid[index] == []:
                app.player.craftGrid[index] = copy.copy(app.player.inventoryHold)
                app.player.inventoryHold = []
            elif type(app.player.craftGrid[index][0]) == type(app.player.inventoryHold):
                app.player.inventory[index].extend(copy.copy(app.player.inventoryHold))
                app.player.inventoryHold = []
            else:
                temp = copy.copy(app.player.craftGrid[index])
                app.player.craftGrid[index] = copy.copy(app.player.inventoryHold)
                app.player.inventoryHold = temp
    initPossibleCrafts(app)


def displayCraftedItem(app, item, number):
    app.player.craftGrid[9] = [copy.copy(item) for i in range(number)]

def depleteCraft(app):
    for i in range(9):
        # if app.player.craftGrid[i] != [] and isinstance(app.player.craftGrid[i][0], LogBlock):
        #         app.player.craftGrid[i].pop()
        # if app.player.craftGrid[i] != [] and isinstance(app.player.craftGrid[i][0], WoodPlankBlock):
        #         app.player.craftGrid[i].pop()
        if app.player.craftGrid[i] != []:
            app.player.craftGrid[i].pop()

def splitItemHand(app):
    row, col = app.craftSelect
    index = InvToList(row, col)
    if app.player.inventoryHold == [] and app.player.inventory[index] != []:
            slice = len(app.player.inventory[index]) // 2
            app.player.inventoryHold = app.player.inventory[index][:slice]
            app.player.inventory[index] = app.player.inventory[index][slice:]

def splitItemCraft(app):
    row, col = app.craftSelect[0] % 999, app.craftSelect[1] % 999
    index = craftToList(row, col)
    if app.player.inventoryHold == [] and app.player.craftGrid[index] != []:
            slice = len(app.player.craftGrid[index]) // 2
            app.player.inventoryHold = app.player.craftGrid[index][:slice]
            app.player.craftGrid[index] = app.player.craftGrid[index][slice:]

def clearCraftSlot(app):
    app.player.craftGrid[9] = []

# Returns a list of objects that the player can craft
def initPossibleCrafts(app):
    crafts = {"Log":0, "Stick":0, "Stone":0, "WoodenPlank":0}

    for i in range(9):
        if app.player.craftGrid[i] != [] and isinstance(app.player.craftGrid[i][0], LogBlock):
            crafts["Log"] += 1
        if app.player.craftGrid[i] != [] and isinstance(app.player.craftGrid[i][0], StickItem):
            crafts["Stick"] += 1
        if app.player.craftGrid[i] != [] and isinstance(app.player.craftGrid[i][0], StoneBlock):
            crafts["Stone"] += 1
        if app.player.craftGrid[i] != [] and isinstance(app.player.craftGrid[i][0], WoodPlankBlock):
            crafts["WoodenPlank"] += 1

    for i in range(9):
        # Recipe for wooden planks
        if app.player.craftGrid[i] != []:
            if crafts["Log"] == 1: 
                displayCraftedItem(app, WoodPlankBlock(app), 4)
            if crafts["WoodenPlank"] == 2: 
                displayCraftedItem(app, StickItem(app), 4)
            if crafts["Stick"] == 2 and crafts["Stone"] == 3: 
                displayCraftedItem(app, StoneAxeItem(app), 1)
            
# Maps list index to the inventory row col
def ListToInv(index):
    row = index % 9
    col = index - row
    return row, col

# Maps inventory row col to list index
def InvToList(row, col):
    index = row*9 + col
    return index

# Same for crafting menu
def listToCraft(index):
    row = index % 3
    col = index - row
    return (row, col)

def craftToList(row, col):
    index = row*3 + col
    if (row, col) == (4, 4):
        return 9
    return index

def drawInventory(app, canvas):
    rows, cols = 4, 9
    for row in range(rows):
        for col in range(cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            index = InvToList(row, col)

            gridWidth  = app.width - 2*app.craftMargin
            gridHeight = app.height - 2*app.craftMargin
            cellWidth  = gridWidth / cols
            cellHeight = gridHeight / rows
            if (row, col) == app.craftSelect: fill = 'Red'
            else: fill = ""
            canvas.create_rectangle(x0, y0+150, x1, y1+150, fill=fill)
            if app.player.inventory[index] != []:
                item = str(app.player.inventory[index][0])
                num = len(app.player.inventory[index])
                canvas.create_text(x0 + cellWidth/2, y0+150+cellHeight/2, text=f"{item} {num}")
    if app.player.inventoryHold != []:
        canvas.create_text(50, 50, text=f"{app.player.inventoryHold[0]}: {len(app.player.inventoryHold)}")
    else:
        canvas.create_text(50, 50, text=f"Holding Nothing")

def drawCraftMenu(app, canvas):
    cellWidth  = (app.width - 2*app.craftMargin) / 9
    cellHeight = (app.height - 2*app.craftMargin) / 4
    leftMargin = app.craftMargin
    topMargin = 20
    # Draw a 3x3 grid, offset from the centre
    for row in range(3):
        for col in range(3):
            index = craftToList(row, col)
            if (row+999, col+999) == app.craftSelect: fill = 'Red'
            else: fill = ""
            (x0, y0, x1, y1) = (leftMargin+cellWidth*col, topMargin+cellHeight*row, 
                        leftMargin+cellWidth*(1+col), topMargin+cellHeight*(1+row))
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
            if app.player.craftGrid[index] != []:
                item = str(app.player.craftGrid[index][0])
                num = len(app.player.craftGrid[index])
                canvas.create_text(x0 + cellWidth/2, y0+cellHeight/2, text=f"{item} {num}")
    
    # Hard coding the crafted item slot
    if app.craftSelect == (999+4, 999+4): fill = "Red"
    else: fill = ""
    (x0, y0, x1, y1) = (leftMargin+cellWidth*5, topMargin+cellHeight*1, leftMargin+cellWidth*6, topMargin+cellHeight*2)
    canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
    index = 9
    if app.player.craftGrid[index] != []:
        item = str(app.player.craftGrid[index][0])
        num = len(app.player.craftGrid[index])
        canvas.create_text(x0 + cellWidth/2, y0+cellHeight/2, text=f"{item} {num}")




