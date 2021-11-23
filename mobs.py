from player import *
from entities import *

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
        x0 = x - (self.playerWidth/2) - self.app.scrollX
        y0 = y - (self.playerLen/2) - self.app.scrollY
        x1 = x + (self.playerWidth/2) - self.app.scrollX
        y1 = y + (self.playerLen/2) - self.app.scrollY
        canvas.create_rectangle(x0, y0, x1, y1, fill='Lime')


#############################
# BFS PATHFINDING ALGORITHM #
#############################
    
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
            if 0 <= drow+row < self.app.rows and 0 <= dcol+col < self.app.cols and isinstance(self.app.grid[row+drow][col+dcol], AirBlock):
                    neighbours.append((row+drow, col+dcol))
        return neighbours

    # Traces back the path given a dictionary that has start - target path
    def tracePath(self, graph, startNode, targetNode):
        # print(startNode, targetNode)
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
        limitRow, limitCol = 50, 50
        
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
                    graph.addEdge((currRow, currCol), neighbour)
        
    # TODO: make mob move towards player at each tick or something
    def getC(self, row, col):
        x0, y0, x1, y1 = GetBounds.Cell(self.app, row, col)
        cx = self.playerLen/2 + x0
        cy = self.playerLen/2 + y0
        return cx, cy

    def takeStep(self):
        path = self.generateGraph()
        if path != None and len(path) != 0:
            row, col = path[0][0], path[0][1]
            cx, cy = self.getC(row, col)
            self.playerX = cx
            self.playerY = cy

    def inflictDamage(self):
        currRow, currCol = GetBounds.RowCol(self.app, self.playerX, self.playerY)
        if self.nearPlayer(currRow, currCol):
            self.app.player.health -= 3


# Keep a set of all vertices that are visited, initially empty
# Have a queue of unvisited neighbors (initially just the start node)
# Extract the current node from the front of the queue
# Skip if the current node has already been visited, otherwise mark it as visited
# Stop if the current node = the target node
# Loop over the neighbors of the current node
# If they are unvisited, add them to the end of the queue
# Repeat 3-7 until the queue is empty
# This is typically not done with recursion

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

# Simple zombie pathfinding:
# if a shortest path exist to the player, then take it
# paths that dont qualify include blocks that are more than 2 high (cant jump over) and also ones that have 5+ blocks of falling
# otherwise, stand on the block closest to the player
# 1. generate the graph with nodes = airblocks with solid block below or two blocks beneath