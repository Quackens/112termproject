from entities import *

# Generates a chunk
def genChunk(app, rows, cols):
    chunk = [[]*cols for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            # NOTE: For now, hard code the air to grassblock boundaries, fix later
            if row > (app.rows // 2):
                chunk[row].append(GrassBlock(app, row, col))
            else:
                chunk[row].append(AirBlock(app, row, col))
    return chunk



# Cave generation
# https://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664

# Pre mvp pathfinding: bfs
# post mvp: a star and dijkstra's (digging through walls, blocks have huge weights)

