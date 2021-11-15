from entities import *

# Generates a chunk
def genChunk(app, rows, cols):
    chunk = [[]*cols for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            # NOTE: For now, hard code the air to grassblock boundaries, fix later
            # Add world gen functions here
            if row == (app.rows // 2) + 1:
                chunk[row].append(GrassBlock(app, row, col))
            elif row <= (app.rows // 2):
                chunk[row].append(AirBlock(app, row, col))
            else:
                chunk[row].append(DirtBlock(app, row, col))
    return chunk



# Cave generation
# https://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664

# If a living cell has less than two living neighbours, it dies.
# If a living cell has two or three living neighbours, it stays alive.
# If a living cell has more than three living neighbours, it dies.
# If a dead cell has exactly three living neighbours, it becomes alive.

# Research
# https://www.reddit.com/r/proceduralgeneration/comments/3yh2ze/terraria_cave_generation/


# Pre mvp pathfinding: bfs
# post mvp: a star and dijkstra's (digging through walls, blocks have huge weights)

