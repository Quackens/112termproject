import copy

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

# Obtained from course notes, modified
def getCell(app, x, y):
    rows, cols = 4, 9
    if (not pointInGrid(app, x, y)):
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
    if app.player.inventoryHold == []:
        app.player.inventoryHold = copy.copy(app.player.inventory[index])
        app.player.inventory[index] = []
    else:
        if app.player.inventory[index] == []:
            app.player.inventory[index] = copy.copy(app.player.inventoryHold)
            app.player.inventoryHold = []
        elif type(app.player.inventory[index][0]) == type(app.player.inventoryHold[0]):
            app.player.inventory[index].extend(copy.copy(app.player.inventoryHold))
            app.player.inventoryHold = []
        else:
            temp = copy.copy(app.player.inventory[index])
            app.player.inventory[index] = copy.copy(app.player.inventoryHold)
            app.player.inventoryHold = temp

# Maps list index to the inventory row col
def ListToInv(index):
    row = index % 9
    col = index - row
    return row, col

# Maps inventory row col to list index
def InvToList(row, col):
    index = row*9 + col
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
    canvas.create_text(50, 50, text=f"{app.player.inventoryHold[0]}: {len(app.player.inventoryHold)}")

# TODO: Make a crafting menu
def drawCraftMenu(app, canvas):
    cellWidth  = app.width - 2*app.craftMargin / 9
    cellHeight = app.height - 2*app.craftMargin / 4

