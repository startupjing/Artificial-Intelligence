# baselineTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  wrapper = StateWrapper()
  agents = [MyAgent(firstIndex), MyAgent(secondIndex)]
  for agent in agents:
    agent.SetStateWrapper(wrapper)
  return agents

##########
# Agents #
##########

class MyAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
  def SetStateWrapper(self, wrapper):
    self.wrapper = wrapper
  def registerInitialState(self, gameState):
    self.red = gameState.isOnRedTeam(self.index)
    self.distancer = distanceCalculator.Distancer(gameState.data.layout)

    # comment this out to forgo maze distance computation and use manhattan distances
    self.distancer.getMazeDistances()

    self.wrapper.Update(self.index, gameState, None, self)
    self.wrapper.Initialize()
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    successor = self.getSuccessor(gameState, action)
    
    self.wrapper.Update(self.index, successor, gameState, self)
    
    if not (-2 < False and False < True and True < 2):
      sorted(None) #assert
    
    if self.wrapper.AgentKilled(self.index):
      return (-100,)
      
    numRemainingFood = len(self.wrapper.FoodListForAgent(self.index))
    if numRemainingFood <= 2:
      return (100,)
    
    agentPos = self.wrapper.GetAgentPosition(self.index)
    ghostPoses = []
    if not self.wrapper.AgentSafe(self.index, agentPos):
      for opponentIndex in self.wrapper.GetOpponentIndices():
        opponentPos = self.wrapper.GetAgentPosition(opponentIndex)
        if opponentPos is None:
          continue
        if util.manhattanDistance(agentPos, opponentPos) <= 6 and self.wrapper.GetAgentTimer(opponentIndex) < 2:
          ghostPoses.append(opponentPos)
          if util.manhattanDistance(agentPos, opponentPos) <= 1:
            return (-90,)
    for opponentIndex in self.wrapper.GetOpponentIndices():
      if self.wrapper.AgentKilled(opponentIndex):
        return (90,)
    scoring = self.wrapper.Scored()
    
    if len(ghostPoses) > 0:
      best = (False, 0, -1000) # best safe, best score, best length
      for destination, utility in self.wrapper.ComputeBestPathUtilityMap(agentPos, self.index, ghostPoses).items():
        if utility is None:
          continue
        safe = self.wrapper.AgentSafe(self.index, destination) or destination in self.wrapper.PelletListForAgent(self.index)
        score, pathlength = utility
        if numRemainingFood - score <= 2:
          safe = True #win
        if scoring:
          score += 1
        value = (safe, score, -pathlength)
        if safe:
          value = (True, 0, 0)
        if best is None or value > best:
          best = value
    else:
      best = (True, 0, 0)
      
    partnerIndex = (self.index + 2) % 4
    partnerPos = self.wrapper.GetAgentPosition(partnerIndex)
    partnerDist = self.wrapper.GetMazeDistance(agentPos, partnerPos)
    
    foodMinDist = self.wrapper.DistanceToNearestFoodWithPartner(partnerIndex)

    
    best = (best[0], -foodMinDist + 0.2 * min(partnerDist, 15), best[1], best[2])
    
    # print self.index, action, agentPos, best
    return best
    
    
class StateWrapper:
  def __init__(self):
    self.initialized = False
  def Initialize(self):
    if self.initialized is True:
      return
    self.initialized = True
    gameWalls = self.nextState.getWalls()
    self.height = gameWalls.height
    self.width = gameWalls.width
  def Update(self, index, nextState, prevState, object):
    self.index = index
    self.nextState = nextState
    self.prevState = prevState
    self.object = object
  def GetOpponentIndices(self):
    gameState = self.nextState
    opponentIndices = self.object.getOpponents(gameState)
    return opponentIndices
  def GetAgentPosition(self, agentIndex):
    return self.nextState.getAgentState(agentIndex).getPosition()
  def GetAgentTimer(self, agentIndex):
    return self.nextState.getAgentState(agentIndex).scaredTimer
  def GetMazeDistance(self, pos1, pos2):
    return self.object.getMazeDistance(pos1, pos2)
  def DistanceToNearestGhost(self):
    gameState = self.nextState
    object = self.object
    index = self.index
    agentState = gameState.getAgentState(index)
    agentPos = agentState.getPosition()
    opponentStates = [gameState.getAgentState(i) for i in object.getOpponents(gameState)]
    invaders = [a for a in opponentStates if a.isPacman and a.getPosition() != None]
    ghosts = [a for a in opponentStates if not a.isPacman and a.scaredTimer < 2 and a.getPosition() != None]
    if agentState.isPacman and len(ghosts) > 0:
      ghostMinDist = min(object.getMazeDistance(agentPos, a.getPosition()) for a in ghosts)
    else:
      ghostMinDist = 6
    return ghostMinDist
  def DistanceToNearestFood(self):
    gameState = self.nextState
    object = self.object
    agentIndex = self.index
    agentState = gameState.getAgentState(agentIndex)
    agentPos = agentState.getPosition()
    if self.Scored():
      return 0
    foodMinDist = 1000
    foodMap = self.FoodMapForAgent(gameState, agentIndex)
    for foodPos, isFood in foodMap.items():
      if not isFood:
        continue
      foodDist = object.getMazeDistance(agentPos, foodPos)
      if foodDist < foodMinDist:
        foodMinDist = foodDist
    return foodMinDist
  def DistanceToNearestFoodWithPartner(self, partnerIndex):
    gameState = self.nextState
    object = self.object
    agentIndex = self.index
    agentState = gameState.getAgentState(agentIndex)
    agentPos = agentState.getPosition()
    if self.Scored():
      return 0
    foodMap = self.FoodMapForAgent(gameState, agentIndex)
    foodList = [foodPos for foodPos, isFood in foodMap.items() if isFood]
    if len(foodList) == 0:
      return 99999
    partnerState = gameState.getAgentState(partnerIndex)
    partnerPos = partnerState.getPosition()
    agentDists = [object.getMazeDistance(agentPos, foodPos) for foodPos in foodList]
    partnerDists = [object.getMazeDistance(partnerPos, foodPos) for foodPos in foodList]
    if min(agentDists) < min(partnerDists):
      foodMinDist = min(agentDists)
    else:
      nextPos = foodList[partnerDists.index(min(partnerDists))]
      nextDists = [object.getMazeDistance(nextPos, foodPos) for foodPos in foodList]
      threshold = 1.0 * sum(nextDists) / len(nextDists)
      myFoodIndices = [i for i in range(len(foodList)) if nextDists[i] >= threshold or nextDists[i] >= agentDists[i]]
      foodMinDist = min(agentDists[i] for i in myFoodIndices)
    return foodMinDist
  def AgentKilled(self, agentIndex):
    if agentIndex in self.GetOpponentIndices():
      agentPos = self.nextState.getAgentState(self.index).getPosition()
      prevOpponentPos = self.prevState.getAgentState(agentIndex).getPosition()
      if prevOpponentPos is not None and agentPos == prevOpponentPos:
        return True
    else:
      agentPos = self.nextState.getAgentState(agentIndex).getPosition()
      prevPos = self.prevState.getAgentState(agentIndex).getPosition()
      if util.manhattanDistance(agentPos, prevPos) > 1:
        return True
    return False
  def FoodMapForAgent(self, gameState, agentIndex):
    height = self.height
    width = self.width
    teamblue = agentIndex in gameState.getBlueTeamIndices()
    gameFoods = gameState.getRedFood() if teamblue else gameState.getBlueFood() # get list of edible foods
    foodMap = { (x, y) : gameFoods[x][y] for x in range(width) for y in range(height) }
    return foodMap
  def FoodListForAgent(self, agentIndex):
    foodMap = self.FoodMapForAgent(self.nextState, agentIndex)
    return [foodPos for foodPos, isFood in foodMap.items() if isFood]
  def PelletListForAgent(self, agentIndex):
    gameState = self.nextState
    teamblue = agentIndex in gameState.getBlueTeamIndices()
    pelletList = gameState.getRedCapsules() if teamblue else gameState.getBlueCapsules()
    return pelletList
  def AgentSafe(self, agentIndex, pos):
    gameState = self.nextState
    teamblue = agentIndex in gameState.getBlueTeamIndices()
    agentState = gameState.getAgentState(agentIndex)
    oldPos = agentState.getPosition()
    object = self.object
    if agentState.scaredTimer > object.getMazeDistance(oldPos, pos):
      return False
    if teamblue and pos[0] >= self.width / 2:
      return True
    if not teamblue and pos[0] < self.width / 2:
      return True
    return False
  def Scored(self):
    agentIndex = self.index
    agentPos = self.nextState.getAgentState(agentIndex).getPosition()
    prevFoods = self.FoodMapForAgent(self.prevState, agentIndex)
    if prevFoods[agentPos]:
      return True
    return False
  def ComputeBestPathUtilityMap(self, agentPos, agentIndex, enemyPoses):
    gameState = self.nextState
    gameWalls = gameState.getWalls()
    height = self.height
    width = self.width
    wallMap = { (x, y) : gameWalls[x][y] for x in range(width) for y in range(height) }
    foodMap = self.FoodMapForAgent(gameState, agentIndex)
    # distMap: map<coord, (mindist, [numfoodeaten]*6)>
    maxRelaxation = 7
    distMap = { (x, y) : None for x in range(width) for y in range(height) }
    offsets = [ (-1, 0), (0, -1), (0, 1), (1, 0) ]
    neighborMap = { (x, y) : None if wallMap[(x, y)] else [(x + dx, y + dy) for dx, dy in offsets if not wallMap[(x + dx, y + dy)]] for x in range(width) for y in range(height) }
    # bfsQueue: queue<solution: (coord, pathlength, numfoodeaten, parentsolution)>
    queue = []
    queuehead = 0
    queue.append((agentPos, 0, 0, None))
    while queuehead < len(queue):
        node = queue[queuehead]
        pos, dist, score, parent = node
        queuehead += 1
        updated = False
        if distMap[pos] is None:
          mindist = dist
          scorelist = [score] * maxRelaxation
          distMap[pos] = (mindist, scorelist)
          updated = True
        else:
          mindist, scorelist = distMap[pos]
          for relaxation in range(dist - mindist, maxRelaxation):
            if scorelist[relaxation] < score:
              scorelist[relaxation] = score
              updated = True
        if updated:
          # add neighbors
          for pos2 in neighborMap[pos]:
            if foodMap[pos2]:
              scoring = True
              node3 = parent
              for i in range(1, maxRelaxation):
                if node3 is None:
                  break
                pos3, dist3, score3, node3 = node3
                if pos3 == pos2:
                  scoring = False # the food is already eaten
                  break
            else:
              scoring = False
            dist2 = dist + 1
            score2 = score + 1 if scoring else score
            parent2 = node
            queue.append((pos2, dist2, score2, parent2))
    utilities = {}
    for pos in [ (x, y) for x in range(width) for y in range(height) ]:
      if distMap[pos] is None:
        utilities[pos] = None
        continue
      mindist, scorelist = distMap[pos]
      enemyMinDist = min(self.object.getMazeDistance(pos, a) for a in enemyPoses) if len(enemyPoses) > 0 else 99999
      allowance = enemyMinDist - mindist - 2
      if allowance < 0:
        utilities[pos] = None
      else:
        score = scorelist[min(allowance, maxRelaxation - 1)]
        pathlength = mindist + min(i for i in range(maxRelaxation) if scorelist[i] >= score)
        utilities[pos] = (score, pathlength)
    return utilities

class OffensiveReflexAgent(MyAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1}

class DefensiveReflexAgent(MyAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}
