from cmu_112_graphics import *


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
    def __init__(self, app, row=0, col=0):
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
    def __init__(self, app, row=0, col=0):
        super().__init__(app, row, col)
        self.texture = "Green"
    
    def __repr__(self):
        return 'GrassBlock'

class AirBlock(Block):
    def __init__(self, app, row=0, col=0):
        super().__init__(app, row, col)
        self.texture = "White"

    def render(self, canvas):
        pass

    def __repr__(self):
        return 'AirBlock'

class DirtBlock(Block):
    def __init__(self, app, row=0, col=0):
        super().__init__(app, row, col)
        self.texture = "saddle brown"

    def __repr__(self):
        return 'DirtBlock'

class StoneBlock(Block):
    def __init__(self, app, row=0, col=0):
        super().__init__(app, row, col)
        self.texture = "Grey"

    def __repr__(self):
        return 'StoneBlock'

class LogBlock(Block):
    def __init__(self, app, row=0, col=0):
        super().__init__(app, row, col)
        self.texture = "Brown"

    def __repr__(self):
        return 'LogBlock'

class LeafBlock(Block):
    def __init__(self, app, row=0, col=0):
        super().__init__(app, row, col)
        self.texture = "Maroon"

    def __repr__(self):
        return 'LeafBlock'

class WoodPlankBlock(Block):
    def __init__(self, app, row=0, col=0):
        super().__init__(app, row, col)
        self.texture = "Blue"

    def __repr__(self):
        return 'WoodPlankBlock'


