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

# Class for bats (flying things that attack you)
# Since inheriting from player, just pretend mobs are player entities too
class Bat(Player):
    def __init__(self, app, posX, posY):
        super().__init__()
        self.playerX = posX
        self.playerY = posY
        self.playerLen = app.blockLen
        self.playerWidth = app.blockLen
    
    def render(self, canvas):
        x = self.playerX
        y = self.playerY
        canvas.create_rectangle(x-self.playerWidth/2, y-self.playerLen/2,
                                x+self.playerWidth/2, y+self.playerLen/2, fill='Lime')
    # Returns whether the bat is close to the player (within a block radius of the player)
    def nearPlayer(self, row, col):
        playerX, playerY = self.app.playerX, self.app.playerY
        mobX, mobY = self.playerX, self.playerY
        if abs(playerX - mobX) < self.app.blockLen and abs(playerY - mobY) < self.app.blockLen:
            return True
        else:
            return False
    # Assume that the Bat can reach the player on every instance
    # Loop through adjacent cells
    def getNeighbouringBlocks(self, row, col):
        neighbours = []
        for (drow, dcol) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            if isinstance(self.app.grid[row+drow][col+dcol], AirBlock):
                neighbours.append((row+drow, col+dcol))
        return neighbours

# TODO:
    def tracepath(self, graph, startNode, targetNode):
        # go through each key's dictionary and find the target node
        path = []
        for node in graph.table:
                if targetNode in graph.table[node]:
                    path.append(node)
                    targetNode = node
        
        while (targetNode != startNode):
            
            
            # Keep going back until the targetNode hits startNode, then return reversed list
                if targetNode in graph.table[node]:
                    path.append(node)
                    targetNode = node
        path.append(startNode)
        path.reverse()
        return path


    def generatePath(self):
        startRow, startCol = self.getPlayerBounds()
        targetRow, targetCol = GetBounds.RowCol(self.app, self.app.playerX, self.app.playerY)
        path = Graph()
        queue = [(startRow, startCol)]
        visited = set()
        passes = 0
        while len(queue) != 0:
            currRow, currCol = queue.pop(0)
            if (currRow, currCol) in visited:
                continue
            elif (neighbour[0], neighbour[1]) == (targetRow, targetCol):
                    return self.tracePath(path, (startRow, startCol), (targetRow, targetCol))
            
            neighbours = self.getNeighbouringBlocks(currRow, currCol)
            for neighbour in neighbours:
                if neighbour not in visited:
                    path.addEdge((startRow, startCol), neighbour)
                    queue.append(neighbour)
            passes += 1
            print(path) # for testing
            if passes == 100:
                break
        
                    



# Keep a set of all vertices that are visited, initially empty
# Have a queue of unvisited neighbors (initially just the start node)
# Extract the current node from the front of the queue
# Skip if the current node has already been visited, otherwise mark it as visited
# Stop if the current node = the target node
# Loop over the neighbors of the current node
# If they are unvisited, add them to the end of the queue
# Repeat 3-7 until the queue is empty
# This is typically not done with recursion

# Simple zombie pathfinding:
# if a shortest path exist to the player, then take it
# paths that dont qualify include blocks that are more than 2 high (cant jump over) and also ones that have 5+ blocks of falling
# otherwise, stand on the block closest to the player
# 1. generate the graph with nodes = airblocks with solid block below or two blocks beneath


# EASY: MAKE a 'bird' that flies to the player
# Treat all air blocks as nodes
# Adjacent nodes are air blocks that are NSEW to the central block


# NB: since the player is always moving, update the pathfinding every few 'ticks' to set a new path

# Taken from the mini lecture powerpoint
class Graph(object):
    def __init__(self):
        self.table = dict()
    
    def addEdge(self, nodeA, nodeB, weight=1):
        if nodeA not in self.table:
            self.table[nodeA] = {}
        if nodeB not in self.table:
            self.table[nodeB] = {}

        # Not used for BFS
        self.table[nodeA][nodeB] = weight
        self.table[nodeA][nodeB] = weight

    def getEdge(self, nodeA, nodeB):
        return self.table[nodeA][nodeB]
    
    def getNodes(self):
        return list(self.table)
    
    def getNeighbours(self, node):
        return set(self.table[node])