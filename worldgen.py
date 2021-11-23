from entities import *
import random
import math

def topTerrainGenerator(x, y): #col is x, row is y
    y = 4*math.sin(0.3*x)+0.3*math.cos(5*x)-3*math.sin(0.1*x)+10*math.sin(0.05*x)+0.1*math.sin(5*x)
    return int(y) # col is going to be unaffected, ROW is going to be changed

# Generates a chunk
def genChunk(app, rows, cols):
    chunk = [[]*cols for row in range(rows)]
    groundLevelBase = app.rows // 4
    cave = caveGen(rows, cols)
    for row in range(rows):
        for col in range(cols):
            groundLevel = groundLevelBase + topTerrainGenerator(col, row)
            if row < groundLevel:
                chunk[row].append(AirBlock(app, row, col))
            elif row == groundLevel:
                chunk[row].append(GrassBlock(app, row, col))
            elif groundLevel < row < groundLevel+4:
                chunk[row].append(DirtBlock(app, row, col))
            elif groundLevel+4 <= row < groundLevel+random.randint(6, 10):
                chunk[row].append(StoneBlock(app, row, col))
            else:
                if cave[row][col] == False:
                    chunk[row].append(AirBlock(app, row, col))
                else:
                    chunk[row].append(StoneBlock(app, row, col))
    return chunk

# Cave generation
# https://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664

# My implementation
# 1. Initialize
# Select a rectangular area in app.grid
# Initialize the grid of cells of boolean TRUE or FALSE (dead or alive) based on a chance variable
# 2. Grow the grid
# Do the simulation step for each cell in the grid
# NB: make sure to do the simulation step in the old grid, and append the value in a new copy of the grid

# LET FALSE = EMPTY CELL (dead cell)
# Function that returns amount of True (alive cells) based on probability parameter
# random.uniform method thanks to https://stackoverflow.com/questions/6088077/how-to-get-a-random-number-between-a-float-range
def genBool(probability):
    rand = random.uniform(0, 1)
    if rand < probability:
        return True
    else:
        return False

# returns the number of dead and alive cells in a tuple (dead, alive)
def checkNeighbours(grid, row, col):
    dead = 0
    alive = 0
    rows, cols = len(grid), len(grid[0])
    for drow in [-1, 0, 1]:
        for dcol in [-1, 0, 1]:
            if drow == 0 and dcol == 0:
                continue
            elif rows > row+drow >= 0 and cols > col+dcol >= 0:
                if grid[row+drow][col+dcol] == True: # If alive cell
                    alive += 1
                # else:
                #     alive += 1
    return (dead, alive)

# returns the next growth step of a passed in grid
def growGridStep(grid, rows, cols, maxLivingNeighbours, reviveDeadWithLive):
    result = [[False for col in range(cols)] for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            (dead, alive) = checkNeighbours(grid, row, col)
            # Conditions on living cells:
            if grid[row][col] == True:
                # If a living cell has less than a limit, it dies.
                if alive < maxLivingNeighbours: #or alive > maxLivingNeighbours:
                    result[row][col] = False
                # Otherwise, it stays alive.
                else:
                    result[row][col] = True
            # Conditions on dead cells:
            else:
                # If a dead cell has more than a limit of living neighbours, it becomes alive.
                if alive > reviveDeadWithLive:
                    result[row][col] = True
                else:
                    result[row][col] = False
    return result

# generates cave
def caveGen(rows, cols):
    prevGrid = [[genBool(0.4) for col in range(cols)] for row in range(rows)]
    newGrid = None
    # Parametesdddsddddrs of the cave, don't forget the probability parameter too if u want to use it
    maxLivingNeighbours = 3
    reviveDeadWithLive = 4
    numberOfSteps = 100
    for step in range(numberOfSteps):
        newGrid = growGridStep(prevGrid, rows, cols, maxLivingNeighbours, reviveDeadWithLive)
        prevGrid = newGrid
    return newGrid
        
# TODO: (IDea): start off with solid TRUE blocks when initializing array

# Research
# https://www.reddit.com/r/proceduralgeneration/comments/3yh2ze/terraria_cave_generation/

# Grass level generation: sine + cos waves, noise 
# HIgh frequency = low amplitude and vice versa



