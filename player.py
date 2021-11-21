from entities import *
import copy

# Player class
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

        # player inventory
        self.inventory = dict()
        self.selectedBlock = DirtBlock(self.app)
    
    # Returns the absolute bounds of the player
    def getPlayerBounds(self):
        x0, y0 = self.playerX - self.playerWidth/2, self.playerY - self.playerLen/2
        x1, y1 = self.playerX + self.playerWidth/2, self.playerY+ self.playerLen/2
        return (x0, y0, x1, y1)
   
    # def movePlayerRight(self):
    #     if not self.isRightSideCollision():
    #         self.app.scrollX += 5
    #         self.playerX += 5

    # def movePlayerLeft(self):
    #     if not self.isLeftSideCollision():
    #         self.app.scrollX -= 5
    #         self.playerX -= 5

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

# If the player's feet is On a grass block, then return True:
            # Get the player's bounds, look at the feet bound (x0+x1)/2 and y1
            # If the y1 value coincides with a non air block's y0 value, then return true
            # Which blocks to check? get the bounds of the player, plug it into get row col, and 
                # check surrounding + 1 blocks around the row col block
    def isOnFloor(self):
        (x0, y0, x1, y1) = self.getPlayerBounds()
        # (feet level = y1)
        # Get 2 row col for the lower block of player: one for each corner
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
        if not isinstance(self.currChunk[row][col], AirBlock):
            blockType = str(self.currChunk[row][col])
            oldBlock = self.currChunk[row][col]
            self.app.grid[row][col] = AirBlock(self.app, oldBlock.row, oldBlock.col)
            # Add it to inventory
            if blockType in self.inventory:
                self.inventory[blockType] += 1
            else:
                self.inventory[blockType] = 1

    # TODO: place blocks
    # How to configure ismousepressed right click? differentiate from left click
    def placeBlock(self, x, y):
        row, col = GetBounds.RowCol(self.app, x+self.app.scrollX, y+self.app.scrollY)
        if self.adjacentToBlock(row, col):
            self.selectedBlock.row = row
            self.selectedBlock.col = col
            # newBlock = copy.deepcopy(self.selectedBlock)
            self.app.grid[row][col] = self.selectedBlock
            




    # Makes the player fall as long as their feet are touching air block
    # def gravity(self):
    #     if (not self.isOnFloor()):
    #         self.app.scrollY += 2
    #         self.playerY += 2

    def changeY(self):
        # print("here")
        self.app.scrollY += self.dy
        self.playerY += self.dy

        if not self.isOnFloor():
            self.dy += self.g
        else:
            self.dy = 0
    
    def changeX(self):
        self.playerX += self.dx
        self.app.scrollX += self.dx
        
        
        


            
# Pseudocode for physics
# app.x
# app.y
# app.dx
# app.dy
# app.gravity - 0.98

# def jump(app):
#     app.dy = -3

# def timerfired(app):
#     app.x += app.dx
#     app.y += app.dy

#     if notColliding(app):
#         app.dy += app.gravity