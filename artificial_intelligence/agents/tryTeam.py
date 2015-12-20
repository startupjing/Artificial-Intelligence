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
from game import Grid
import game
from util import nearestPoint

#################
# Team creation #
#################


def createTeam(firstIndex, secondIndex, isRed,
               first = 'ReflexAgent', second = 'ReflexAgent'):
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
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########




class ReflexAgent(CaptureAgent):
    def getAction(self, gameState):
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(self.index)

        # compute score for each action and choose maximizing action
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        maxScore = max(scores)
        bestActions = [a for a, v in zip(legalMoves, scores) if v == maxScore]

        possibleAction = random.choice(bestActions)

        myState = gameState.getAgentState(self.index)
        teammateState = gameState.getAgentState((self.index+2) % gameState.getNumAgents())
        return possibleAction


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

    def getFood(self, gameState):
      teammateIdx = (self.index+2) % gameState.getNumAgents()

      myState = gameState.getAgentState(self.index)
      teammateState = gameState.getAgentState(teammateIdx)

      return self.getMyFood(gameState)


      if myState.isPacman and teammateState.isPacman:
          return self.halfFood(gameState.data.food, teammateIdx<self.index)
      else:
          return self.getMyFood(gameState)

    def getMyFood(self, gameState):
      """
      Returns the food you're meant to eat. This is in the form of a matrix
      where m[x][y]=true if there is food you can eat (based on your team) in that square.
      """
      if self.red:
        return gameState.getBlueFood()
      else:
        return gameState.getRedFood()


    def halfFood(self, grid, isBottom):
      halfway = grid.width / 2
      halfgrid = Grid(grid.width, grid.height, False)
      foodCount = 0

      if not self.red:    xrange = range(halfway)
      else:       xrange = range(halfway, grid.width)

      if isBottom:
          yMin = grid.height / 2
          yMax = grid.height
      else:
          yMin = 0
          yMax = grid.height / 2

      for y in range(yMin, yMax):
        for x in xrange:
          if grid[x][y]:
              halfgrid[x][y] = True
              foodCount

      return halfgrid, foodCount


    def evaluationFunction(self, currentGameState, action):

        successor = self.getSuccessor(currentGameState, action)
        myPos = successor.getAgentState(self.index).getPosition()

        DISTANCE_WITHOUT_FARE = 3
        POSTIVE_SCALE = 1
        NEGATIVE_SCALE = 20

        features = self.getOffensiveFeatures(currentGameState, action)
        weights = self.getOffensiveWeights(currentGameState, action)
        posScore = POSTIVE_SCALE * (features * weights)

        myState = successor.getAgentState(self.index)
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        ghosts = [a for a in enemies if a.getPosition() != None]
        if len(ghosts) > 0:
          ghosts_dists = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
          minDist = min(ghosts_dists)

        defensiveScore = self.getDefensiveFeatures(currentGameState, action) * self.getDefensiveWeights(currentGameState, action)

        if myState.isPacman:
            if len(ghosts) > 0:
              if enemies[ghosts_dists.index(minDist)].scaredTimer >= 5:
                  return posScore
              return -100/minDist
            else:
              return posScore
        else:
            if len(ghosts) > 0:
              halfway = successor.data.food.width/2
              if abs(halfway - myPos[0]) < 2:
                return defensiveScore * 20
              else:
                return defensiveScore
            else:
              return posScore


    def getOffensiveFeatures(self, gameState, action):
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

    def getOffensiveWeights(self, gameState, action):
      return {'successorScore': 100, 'distanceToFood': -1}

    def getDefensiveFeatures(self, gameState, action):
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

    def getDefensiveWeights(self, gameState, action):
      return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}




class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
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
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}


class AgentOne(ReflexAgent):
  def getFood(self, gameState):
      teammateIdx = (self.index+2) % gameState.getNumAgents()

      myState = gameState.getAgentState(self.index)
      teammateState = gameState.getAgentState(teammateIdx)

      myFood,myFoodCount = self.halfFood(gameState.data.food, False)

      if myFoodCount is 0:
          return self.halfFood(gameState.data.food, True)[0]



class AgentTwo(ReflexAgent):
  def getFood(self, gameState):
      teammateIdx = (self.index+2) % gameState.getNumAgents()

      myState = gameState.getAgentState(self.index)
      teammateState = gameState.getAgentState(teammateIdx)

      myFood,myFoodCount = self.halfFood(gameState.data.food, True)

      if myFoodCount is 0:
          return self.halfFood(gameState.data.food, False)[0]

class DefensiveReflexAgent(ReflexCaptureAgent):
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
