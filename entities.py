from cmu_112_graphics import *
from physics import *


class GetBounds(object):
    # Gets coordinates from row, col which stretches off canvas too
    @staticmethod
    def Cell(app, row, col):
        x0 = col * app.blockLen
        x1 = (col+1) * app.blockLen
        y0 = row * app.blockLen
        y1 = (row+1) * app.blockLen
        return (x0, y0, x1, y1)

    # Gets row, col from 2D plane that stretches off canvas
    @staticmethod
    def RowCol(app, x, y):
        row = int(y / app.blockLen)
        col = int(x / app.blockLen)
        return (row, col)

# Blocks
class Block(object):
    def __init__(self, app, row, col):
        self.row = row
        self.col = col
        self.app = app

    def render(self, canvas):
        # calculuate using scrollX, row and col
        (x0, y0, x1, y1) = GetBounds.Cell(self.app, self.row, self.col)
        x0 -= self.app.scrollX
        x1 -= self.app.scrollX
        y0 -= self.app.scrollY
        y1 -= self.app.scrollY
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.texture)

    # Returns absolute bounds of the block
    def getBlockBounds(self):
        return GetBounds.Cell(self.app, self.row, self.col)

class GrassBlock(Block):
    def __init__(self, app, row, col):
        super().__init__(app, row, col)
        self.texture = "Green"
    
    def __repr__(self):
        return 'GrassBlock'

class AirBlock(Block):
    def __init__(self, app, row, col):
        super().__init__(app, row, col)
        self.texture = "White"
    
    def render(self, canvas):
        pass

    def __repr__(self):
        return 'AirBlock'

# # Player class, follows gravity class
# class Player(object):
#     def __init__(self, app, chunk):
#         super().__init__()  # takes in all the attributes from gravity
#         self.app = app
#         self.playerX = app.width // 2
#         self.playerY = app.height // 2
#         self.playerLen = app.blockLen * 2
#         self.playerWidth = app.blockLen
#         self.currChunk = chunk 
#         self.isJumping = False

#     # Returns the absolute bounds of the player
#     def getPlayerBounds(self):
#         x0, y0 = self.playerX - self.playerWidth/2, self.playerY - self.playerLen/2
#         x1, y1 = self.playerX + self.playerWidth/2, self.playerY+ self.playerLen/2
#         return (x0, y0, x1, y1)
   
#     def movePlayerRight(self):
#         self.app.scrollX += 5
#         self.playerX += 5

#     def movePlayerLeft(self):
#         self.app.scrollX -= 5
#         self.playerX -= 5

#     def jumpPlayer(self):
#         if self.isOnFloor():
#             self.app.scrollY -= 30
#             self.playerY -= 30

#     def down(self):
#         self.app.scrollY += 40
#         self.playerY += 40

#     def __repr__(self):
#         return "Player"

#     def render(self, canvas):
#         x = self.app.width//2
#         y = self.app.height//2
#         canvas.create_rectangle(x-self.playerWidth/2, y-self.playerLen/2,
#                                 x+self.playerWidth/2, y+self.playerLen/2, fill='Cyan')

# # If the player's feet is On a grass block, then return True:
#             # Get the player's bounds, look at the feet bound (x0+x1)/2 and y1
#             # If the y1 value coincides with a non air block's y0 value, then return true
#             # Which blocks to check? get the bounds of the player, plug it into get row col, and 
#                 # check surrounding + 1 blocks around the row col block
#     def isOnFloor(self):
#         (x0, y0, x1, y1) = self.getPlayerBounds()
#         # (feet level = y1)

#         # Get row col for the lower block of player
#         # c1row, c1col = GetBounds.RowCol(self.app, (x0+x1)/2, y1)
#         c1row, c1col = GetBounds.RowCol(self.app, x0, y1)
#         c2row, c2col = GetBounds.RowCol(self.app, x1, y1)


#         block1 = self.currChunk[c1row][c1col]
#         block2 = self.currChunk[c2row][c2col]
#         (b1x0, b1y0, b1x1, b1y1) = block1.getBlockBounds()
#         (b2x0, b2y0, b2x1, b2y1) = block2.getBlockBounds()
#         if (not isinstance(block1, AirBlock) and b1y0 == y1) or (not isinstance(block2, AirBlock) and b2y0 == y1):
#             return True
#         else:
#             return False
        
#         # redundant code
#         # for dr in [-1, 0, 1]:
#         #     for dc in [-1, 0, 1]:
#         #         checkRow, checkCol = row + dr, col + dc
#         #         block = self.currChunk[checkRow][checkCol]
#         #         (bx0, by0, bx1, by1) = block.getBlockBounds()
#         #         if not isinstance(block, AirBlock) and by0 == y1:
#         #             return True
#         # return False
            
#     # Makes the player fall as long as their feet are touching air block
#     def gravity(self):
#         if (not self.isOnFloor()):
#             self.app.scrollY += 2
#             self.playerY += 2

#     # when clicked, break the block that is clicked
#     def breakBlock(self, x, y):
#         row, col = GetBounds.RowCol(self.app, x+self.app.scrollX, y+self.app.scrollY)
#         if not isinstance(self.currChunk[row][col], AirBlock):
#             oldBlock = self.currChunk[row][col]
#             self.app.grid[row][col] = AirBlock(self.app, oldBlock.row, oldBlock.col)

        








