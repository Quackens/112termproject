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
    def __init__(self, app, chunk, posX, posY):
        super().__init__(app, chunk)
        self.playerX = posX
        self.playerY = posY
        self.playerLen = self.app.blockLen
        self.playerWidth = self.app.blockLen
    
    def render(self, canvas):
        x, y = self.playerX, self.playerY
        x0 = x-(self.playerWidth/2) - self.app.scrollX
        y0 = y-(self.playerLen/2) - self.app.scrollY
        x1 = x+(self.playerWidth/2) - self.app.scrollX
        y1 = y+(self.playerLen/2) - self.app.scrollY
        canvas.create_rectangle(x0, y0, x1, y1, fill='Lime')

# VVVVVV BFS PATHFINDING ALGORITHM VVVVVVV
# NB: since the player is always moving, update the pathfinding every few 'ticks' to set a new path
    
    # Returns whether the bat is close to the player (within a block radius of the player)
    def nearPlayer(self, mobRow, mobCol):
        playerRow, playerCol = GetBounds.RowCol(self.app, self.app.player.playerX, self.app.player.playerY)
        # For now, nearPlayer returns TRUE if the bat is adjacent to the player within cell coordinates
        if abs(playerRow - mobRow) == 1 and abs(playerCol - mobCol) == 1:
            return True
        else:
            return False

    # Return adjacent cells
    def getNeighbouringBlocks(self, row, col):
        neighbours = []
        for (drow, dcol) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        # for drow in range(-1, 2):
        #     for dcol in range(-1, 2):
            if drow == 0 and dcol == 0:
                continue
            if isinstance(self.app.grid[row+drow][col+dcol], AirBlock):
                neighbours.append((row+drow, col+dcol))
        return neighbours

    # Traces back the path given a dictionary that has start - target path
    def tracePath(self, graph, startNode, targetNode):
        print(startNode, targetNode)
        # print(GetBounds.RowCol(self.app, self.app.player.playerX, self.app.player.playerY))
        path = []
        while targetNode != startNode:
            path.insert(0, targetNode)
            targetNode = graph.table[targetNode]
        return path

    # Generates graph to use for pathfinding
    def generateGraph(self):
        startRow, startCol = GetBounds.RowCol(self.app, self.playerX, self.playerY)
        queue = [(startRow, startCol)]
        graph = Graph()
        graph.addEdge(None, (startRow, startCol))
        visited = set()
        i = 0
        # Also set a limit to how far of blocks the graph is generated
        limitRow, limitCol = 100, 100
        
        while len(queue) != 0:
            currRow, currCol = queue.pop(0)
            if (currRow, currCol) in visited:
                continue
            visited.add((currRow, currCol))
            
            # If the target node is reached, trace back and return the list of nodes to take
            if self.nearPlayer(currRow, currCol):
                return self.tracePath(graph, (startRow, startCol), (currRow, currCol))

            neighbours = self.getNeighbouringBlocks(currRow, currCol)
            for neighbour in neighbours:
                if (neighbour not in visited and abs(neighbour[0] - startRow) < limitRow
                    and abs(neighbour[1] - startCol) < limitCol):
                    queue.append(neighbour)
                    graph.addEdge((currRow, currCol), neighbour) #A = currNode, B = neigihbourNode
            i += 1
            if i == 100000:
                return "Infinite loop"
        print("done")

                    
        # Otherwise, there is no path to the player, idle
        # TODO: make the mob idle

    # TODO: make mob move towards player at each tick or something
    def takeStep(self):
        path = self.generateGraph()
        # Update self.playerX and self.playerY
        print(path)


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


# Inspired by grpah mini lecture, made changes of own for BFS
class Graph(object):
    def __init__(self):
        self.table = dict()
    
    # Directional: nodeA --visits--> nodeB
    # When nodeB is visited from nodeA, nodeB points to nodeA
    def addEdge(self, nodeA, nodeB):
        if nodeA not in self.table:
            self.table[nodeA] = {}
        if nodeB not in self.table:
            self.table[nodeB] = {}
        self.table[nodeB] = nodeA