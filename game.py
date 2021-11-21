from entities import *
from player import *
from mobs import *

# TODO: implement some mob generating mechanic where mobs are 
#       spawned above and below ground relative to where player is
def spawnBat(app, x, y):
    return Bat(app, app.grid, x, y)

# TODO: save game mechanic?
    # Convert block information, inventory, player and mob posiiton into string using repr
    # then store string into a csv file


