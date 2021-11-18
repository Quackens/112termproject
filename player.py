from entities import *

# Player class
class Player(object):
    def __init__(self, app, chunk):
        self.app = app
        self.playerX = app.width // 2
        self.playerY = app.height // 2
        self.playerLen = app.blockLen * 2
        self.playerWidth = app.blockLen
        self.currChunk = chunk 
        self.isJumping = False
        self.dx = 0
        self.dy = 0
    
    # Returns the absolute bounds of the player
    def getPlayerBounds(self):
        x0, y0 = self.playerX - self.playerWidth/2, self.playerY - self.playerLen/2
        x1, y1 = self.playerX + self.playerWidth/2, self.playerY+ self.playerLen/2
        return (x0, y0, x1, y1)
   
    def movePlayerRight(self):
        self.app.scrollX += 5
        self.playerX += 5

    def movePlayerLeft(self):
        self.app.scrollX -= 5
        self.playerX -= 5

    def jumpPlayer(self):
        if self.isOnFloor():
            self.app.scrollY -= 30
            self.playerY -= 30

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
        else:
            return False
    
    # TODO: Side collisions with blocks
    def leftSideCollision(self):
        pass

    def rightSideCollision(self):
        pass

    def headCollision(self):
        pass

    # Makes the player fall as long as their feet are touching air block
    def gravity(self):
        if (not self.isOnFloor()):
            self.app.scrollY += 2
            self.playerY += 2

    # when clicked, break the block that is clicked
    def breakBlock(self, x, y):
        row, col = GetBounds.RowCol(self.app, x+self.app.scrollX, y+self.app.scrollY)
        if not isinstance(self.currChunk[row][col], AirBlock):
            oldBlock = self.currChunk[row][col]
            self.app.grid[row][col] = AirBlock(self.app, oldBlock.row, oldBlock.col)

    # TODO: place blocks
    # How to configure ismousepressed right click? differentiate from left click

# Class for mobs (including enemies)
class Mob(Player):
    def __init__(self, posX, posY):
        super().__init__()
        self.playerX = posX
        self.playerY = posY
    

    def isPlayerReachable(self):
        pass
    
    def findPlayer(self):
        pass


# Pre mvp pathfinding: bfs
# post mvp: a star and dijkstra's (digging through walls, blocks have huge weights)