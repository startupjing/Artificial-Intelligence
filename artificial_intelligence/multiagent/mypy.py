import util
from util import Queue
from game import Actions

def dotProduct(list1, list2):
    return sum(p*q for p,q in zip(list1, list2))

def buildMazeDistanceMap(position, gameState):
    """
      Use BFS to build a map that stores maze distances between position and each point in the layout

    """
    x, y = position
    walls = gameState.getWalls()
    assert not walls[x][y], 'position is a wall: ' + str(position)

    # initialization
    distanceMap = {}
    queue = Queue()
    distance = 0
    queue.push(position)

    while not queue.isEmpty():
    	currPos = queue.pop()

    	if currPos not in distanceMap:
    		distanceMap[currPos] = distance

    		for pos in Actions.getLegalNeighbors(currPos, walls):
    			queue.push(pos)

    	distance += 1

    return distanceMap


