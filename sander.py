from tile import Tile
from constants import TileType, MarkerType, Actions
import random

def determine_flag(view):
    cutoffs = [10, 20, 30, 40]
    weight = getWeight(view)
    if (weight > cutoffs[3]):
        return MarkerType.RED
    else if (weight > cutoffs[2]):
        return MarkerType.ORANGE
    else if (weight > cutoffs[1]):
        return MarkerType.YELLOW
    else if (weight > cutoffs[0]):
        return MarkerType.GREEN
    else:
        return MarkerType.BLUE

def marker_to_flag(marker):
    if (marker == MarkerType.RED):
        return Actions.DROP_RED
    else if (marker = MarkerType.BLUE):
        return Actions.DROP_BLUE
    else if (marker = MarkerType.YELLOW):
        return Actions.DROP_YELLOW
    else if (marker = MarkerType.GREEN):
        return Actions.DROP_GREEN
    else if (marker = MarkerType.ORANGE):
        return Actions.DROP_ORANGE

def get_move(self, view):
    adjacentWeights = weightAdjacent()
    total = 0
    weightList = []
    for i in range (0, 3):
        for j in range(0, 3):
            if (i != 1 and j != 1):
                total = total + adjacentWeights[i][j]
                weightList.append(total)
    rand = random.randint(0, total)
    if (random < weightList[0]):
        action = Actions.MOVE_NW
    else if (random < weightList[1]):
        action = Actions.MOVE_N
    else if (random < weightList[2]):
        action = Actions.MOVE_NE
    else if (random < weightList[3]):
        action = Actions.MOVE_W
    else if (random < weightList[4]):
        action = Actions.MOVE_E
    else if (random < weightList[5]):
        action = Actions.MOVE_SW
    else if (random < weightList[6]):
        action = Actions.MOVE_S
    else:
        action = Actions.MOVE_SE

    currentTile = view[self.fov()][self.fov()][0]
    dropFlag = marker_to_flag(determine_flag(view))
    tileType = currentTile.GetType()
    if (tileType == TileType.Base):
        return (Actions.DROPOFF, dropFlag)
    else if (tileType == TileType.Resource):
        return (Actions.MINE, dropFlag)
    else if (tileType == TileType.Plain):
        return (action, dropFlag)
    else:
        # Current position cannot be mountain
