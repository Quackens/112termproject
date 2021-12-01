##########################################################
# This file contains the player class - stats, movement
##########################################################

from entities import *
import copy

class Player(object):
    def __init__(self, app, chunk):
        self.app = app
        self.playerX = app.width // 2
        self.playerY = app.height // 2
        self.playerLen = app.blockLen * 2
        self.playerWidth = app.blockLen
        self.currChunk = chunk 
        self.dx = 0
        self.dy = 0
        self.g = 1
        self.mouseX = 0
        self.mouseY = 0
        self.health = 1000

        # inventory variables
        self.inventory = [[] for i in range(36)]
        self.inventoryHold = []
        self.selectedStack = 0
        
        # Crafting grid entity
        self.craftGrid = [[] for i in range(10)]
    
    # Returns the absolute bounds of the player
    def getPlayerBounds(self):
        x0, y0 = self.playerX - self.playerWidth/2, self.playerY - self.playerLen/2
        x1, y1 = self.playerX + self.playerWidth/2, self.playerY+ self.playerLen/2
        return (x0, y0, x1, y1)

####################
# Movement
####################
    def movePlayerRight(self, press):
        if not self.isRightSideCollision() and press:
            self.dx = 2
            # self.playerX += self.dx
            # self.app.scrollX += self.dx
            self.app.player.changeX()
        else:
            self.dx = 0
        
    def movePlayerLeft(self, press):
        if not self.isLeftSideCollision() and press:
            self.dx = -2
            # self.playerX += self.dx
            # self.app.scrollX += self.dx
            self.app.player.changeX()
        else:
            self.dx = 0

    def jumpPlayer(self):
        if self.isOnFloor():
            self.dy = -7

# For testing purposes
    def down(self):
        self.app.scrollY += 40
        self.playerY += 40
    def FLY(self):
        self.app.scrollY -= 30
        self.playerY -= 30

    def __repr__(self):
        return "Player"

    def render(self, canvas):
        x = self.app.width//2
        y = self.app.height//2
        canvas.create_rectangle(x-self.playerWidth/2, y-self.playerLen/2,
                                x+self.playerWidth/2, y+self.playerLen/2, fill='Cyan')
    def changeY(self):
        self.app.scrollY += self.dy
        self.playerY += self.dy

        if not self.isOnFloor():
            self.dy += self.g
        else:
            self.dy = 0
    
    def changeX(self):
        self.playerX += self.dx
        self.app.scrollX += self.dx

# If the player's feet is On a grass block, then return True:
            # Get the player's bounds, look at the feet bound (x0+x1)/2 and y1
            # If the y1 value coincides with a non air block's y0 value, then return true
            # Which blocks to check? get the bounds of the player, plug it into get row col, and 
                # check surrounding + 1 blocks around the row col block
    def isOnFloor(self):
        (x0, y0, x1, y1) = self.getPlayerBounds()
        c1row, c1col = GetBounds.RowCol(self.app, x0 + 0.05, y1)
        c2row, c2col = GetBounds.RowCol(self.app, x1 - 0.05, y1)

        block1 = self.currChunk[c1row][c1col]
        block2 = self.currChunk[c2row][c2col]
        (b1x0, b1y0, b1x1, b1y1) = block1.getBlockBounds()
        (b2x0, b2y0, b2x1, b2y1) = block2.getBlockBounds()
        
        if (not isinstance(block1, AirBlock) and b1y0 == y1) or (not isinstance(block2, AirBlock) and b2y0 == y1):
            return True
        elif (not isinstance(block1, AirBlock) and b1y0 < y1 < b1y1) or (not isinstance(block2, AirBlock) and b2y0 < y1 < b2y1):
            self.adjustHeight(y1, b1y0)
            return True 
        else:
            return False
    
    def adjustHeight(self, posY, blockY):
        adjustY = blockY - posY # Going to be negative since posY > blockY
        self.playerY += adjustY
        self.app.scrollY += adjustY
    
    def adjustLeft(self, posX, blockX):
        adjustX = blockX - posX # posX < blockX
        self.playerX += adjustX
        self.app.scrollX += adjustX

    def adjustRight(self, posX, blockX):
        adjustX = blockX - posX # posX > blockX
        self.playerX += adjustX
        self.app.scrollX += adjustX

    # TODO: Side collisions with blocks

    # If colliding with blocks, return True
    def isLeftSideCollision(self):
        (x0, y0, x1, y1) = self.getPlayerBounds()
        c1row, c1col = GetBounds.RowCol(self.app, x0 - 0.2, y0 + 0.05)   # top left side
        c2row, c2col = GetBounds.RowCol(self.app, x0 - 0.2, y1 - 0.05)   # bottom left side
        block1 = self.currChunk[c1row][c1col]
        block2 = self.currChunk[c2row][c2col]
        (b1x0, b1y0, b1x1, b1y1) = block1.getBlockBounds()
        (b2x0, b2y0, b2x1, b2y1) = block2.getBlockBounds()

        if (not isinstance(block1, AirBlock) and b1x1 == x0) or (not isinstance(block2, AirBlock) and b2x1 == x0):
            return True
        elif (not isinstance(block1, AirBlock) and b1x0 < x0 < b1x1) or (not isinstance(block2, AirBlock) and b2x0 < x0 < b2x1):
            self.adjustLeft(x0, b1x1)
            return True
        else:
            return False
    
    def isRightSideCollision(self):
        (x0, y0, x1, y1) = self.getPlayerBounds()
        c1row, c1col = GetBounds.RowCol(self.app, x1+0.2, y0 + 0.05)   # top right side
        c2row, c2col = GetBounds.RowCol(self.app, x1+0.2, y1 - 0.05)   # bottom right side
        block1 = self.currChunk[c1row][c1col]
        block2 = self.currChunk[c2row][c2col]
        (b1x0, b1y0, b1x1, b1y1) = block1.getBlockBounds()
        (b2x0, b2y0, b2x1, b2y1) = block2.getBlockBounds()
        if (not isinstance(block1, AirBlock) and b1x0 == x1) or (not isinstance(block2, AirBlock) and b2x0 == x1):
            return True
        elif (not isinstance(block1, AirBlock) and b1x0 < x1 < b1x1) or (not isinstance(block2, AirBlock) and b2x0 < x1 < b2x1):
            self.adjustRight(x1, b1x0)
            return True
        else:
            return False

    def isHeadCollision(self):
        (x0, y0, x1, y1) = self.getPlayerBounds()
        c1row, c1col = GetBounds.RowCol(self.app, x0 + 0.05, y0)
        c2row, c2col = GetBounds.RowCol(self.app, x1 - 0.05, y0)


########################
# Player Interactions
########################

    # highlights block selected by player
    def highlightBlock(self, canvas, x, y):
        row, col = GetBounds.RowCol(self.app, x+self.app.scrollX, y+self.app.scrollY)
        if self.blockInRange(row, col) and not isinstance(self.currChunk[row][col], AirBlock):
            x0, y0, x1, y1 = GetBounds.Cell(self.app, row, col)
            x0 -= self.app.scrollX
            x1 -= self.app.scrollX
            y0 -= self.app.scrollY
            y1 -= self.app.scrollY
            canvas.create_rectangle(x0, y0, x1, y1, outline='red', width=5)
    
    # if block is in breaking distance of player
    def blockInRange(self, row, col):
        radius = 4
        (px0, py0, px1, py1) = self.app.player.getPlayerBounds()
        playerRow, playerCol = GetBounds.RowCol(self.app, px0 + self.app.blockLen/2, py0 + self.app.blockLen)
        # print(abs(playerRow - row), abs(playerCol - col))
        if abs(playerRow - row) < radius and abs(playerCol - col) < radius:
            return True
        else:
            return False
    
    # returns whether block is adjacent to non airblock: block can be placed
    def adjacentToBlock(self, row, col):
        for drow, dcol in [(1,0), (0,1), (-1,0), (0,-1)]:
            if not isinstance(self.currChunk[drow+row][dcol+col], AirBlock):
                return True
        return False

    # when clicked, break the block that is clicked
    # And also add a block to inventory
    def breakBlock(self, x, y):
        row, col = GetBounds.RowCol(self.app, x+self.app.scrollX, y+self.app.scrollY)
        if not isinstance(self.currChunk[row][col], AirBlock) and self.blockInRange(row, col):
            oldBlock = self.currChunk[row][col]
            self.addBlock(oldBlock)
            self.app.grid[row][col] = AirBlock(self.app, oldBlock.row, oldBlock.col)
            # Add it to inventory


    def attackBlock(self, x, y):
        attackRow, attackCol = GetBounds.RowCol(self.app, x+self.app.scrollX, y+self.app.scrollY)
        i = 0
        if self.blockInRange(attackRow, attackCol):
            while i < len(self.app.mobs):
                mob = self.app.mobs[i]
                mobRow, mobCol = GetBounds.RowCol(self.app, mob.playerX, mob.playerY)
                if (attackRow, attackCol) == (mobRow, mobCol):
                    self.app.mobs.pop(i)
                else:
                    i += 1
                
    def placeBlock(self, x, y):
        row, col = GetBounds.RowCol(self.app, x+self.app.scrollX, y+self.app.scrollY)
        if (self.inventory[self.selectedStack] != [] and self.blockInRange(row, col) 
            and self.adjacentToBlock(row, col)):
            newBlock = self.inventory[self.selectedStack].pop()
            newBlock.row = row
            newBlock.col = col
            self.app.grid[row][col] = newBlock

########################
# Inventory Management
########################

    # When breaking block, appends the block to the appropriate 'stack' in inventory
    def addBlock(self, block):
        for i in range(36):
            if (not self.inventory[i] != []) or type(self.inventory[i][0]) == type(block):
                self.inventory[i].append(block)
                return
        # Find the nearest empty list and add the new block in if no stack
        for i in range(36):
            if self.inventory[i] == []:
                self.inventory[i].append(block)
                
    def switchTool(self, tool):
        self.selectedStack = tool - 1


    
