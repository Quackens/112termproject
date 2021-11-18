def getNeighbouringBlocks(row, col):
    neighbours = []
    for (drow, dcol) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        neighbours.append((row+drow, col+dcol))
    return neighbours

print(getNeighbouringBlocks(4, 5))