# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
import mypy

from game import Agent


class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    DISTANCE_WITHOUT_FARE = 3
    POSTIVE_SCALE = 50
    NEGATIVE_SCALE = 500

    # compute score for negative influence
    ghostDists = [manhattanDistance(newPos, ghost_pos) for ghost_pos in successorGameState.getGhostPositions()]
    ghostDists_min = min(ghostDists) + 1  # plus one to avoid dividing by zero
    negScore = NEGATIVE_SCALE/ghostDists_min
    
    # if min ghost distance is larger than DISTANCE_WITHOUT_FARE, no need to fare
    if ghostDists_min > DISTANCE_WITHOUT_FARE:
      negScore = 0
   
    # compute positive influence
    hasFood = currentGameState.getFood()
    foodPos = []
    # find food positions
    for x in range(hasFood.width):
      for y in range(hasFood.height):
        if hasFood[x][y]:
          foodPos.append((x,y))
    
    foodDists = [manhattanDistance(newPos, food_position) for food_position in foodPos]
    foodDists_min = min(foodDists) + 1  # plus one to avoid dividing by zero
    posScore = POSTIVE_SCALE/foodDists_min

    scores = [posScore, negScore]
    weights = [1, -1]

    return mypy.dotProduct(scores, weights)

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """

    "*** YOUR CODE HERE ***"
    return self.getActionHelper(gameState, self.depth, 0)[1]

  def getActionHelper(self, gameState, depth, agentIndex):

    # useful information to know
    isGhost = (agentIndex != 0)
    numAgents = gameState.getNumAgents()
    legalActions = gameState.getLegalActions(agentIndex)

    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)

    # terminal state
    if gameState.isLose() or gameState.isWin() or depth <= 0 or len(legalActions)==0:
      return self.evaluationFunction(gameState), Directions.STOP

    # compute arguments of next function call
    newAgentIndex = (agentIndex + 1) % numAgents  # round robin
    newDepth = depth - 1 if newAgentIndex < agentIndex else depth # stay at same depth if not finish with all agents

    # compute score for each legal action
    scores = [self.getActionHelper(gameState.generateSuccessor(agentIndex, action), newDepth, newAgentIndex)[0] for action in legalActions]

    # use min/max score depends on whether agent is a min/max player
    if isGhost:
      minScore = min(scores)
      return minScore, legalActions[scores.index(minScore)]
    else:
      maxScore = max(scores)
      return maxScore, legalActions[scores.index(maxScore)]


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    return self.getActionHelper(gameState, self.depth, 0, float("-inf"), float("inf"))[1]


  def getActionHelper(self, gameState, depth, agentIndex, alpha, beta):

    # useful information to know
    isGhost = (agentIndex != 0)
    numAgents = gameState.getNumAgents()
    legalActions = gameState.getLegalActions(agentIndex)

    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)

    # terminal state
    if gameState.isLose() or gameState.isWin() or depth <= 0 or len(legalActions)==0:
      return self.evaluationFunction(gameState), Directions.STOP

    # compute arguments of next function call
    newAgentIndex = (agentIndex + 1) % numAgents  # round robin
    newDepth = depth - 1 if newAgentIndex < agentIndex else depth # stay at same depth if not finish with all agents
    newAlpha = alpha
    newBeta = beta

    # return values
    myAction = Directions.STOP
    myScore = beta if isGhost else alpha

    # compute score for each legal action
    for action in legalActions:
      score = self.getActionHelper(gameState.generateSuccessor(agentIndex, action), newDepth, newAgentIndex, newAlpha, newBeta)[0]
      
      # min player
      if isGhost:
        # update best score and best action so far
        if score < myScore:
          myScore = score
          newBeta = score
          myAction = action
        # no need to continue
        if myScore <= alpha:
          return alpha, myAction

      # max player
      else:
        # updat best score and best action so far
        if score > myScore:
          myScore = score
          newAlpha = score
          myAction = action
        # no need to continue
        if myScore >= beta:
          return beta, myAction

    return myScore, myAction

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    return self.getActionHelper(gameState, self.depth, 0)[1]

  def getActionHelper(self, gameState, depth, agentIndex):

    # useful information to know
    isRandomGhost = (agentIndex != 0)
    numAgents = gameState.getNumAgents()
    legalActions = gameState.getLegalActions(agentIndex)

    if Directions.STOP in legalActions:
      legalActions.remove(Directions.STOP)

    # terminal state
    if gameState.isLose() or gameState.isWin() or depth <= 0 or len(legalActions)==0:
      return self.evaluationFunction(gameState), Directions.STOP

    # compute arguments of next function call
    newAgentIndex = (agentIndex + 1) % numAgents  # round robin
    newDepth = depth - 1 if newAgentIndex < agentIndex else depth # stay at same depth if not finish with all agents

    # compute score for each legal action
    scores = [self.getActionHelper(gameState.generateSuccessor(agentIndex, action), newDepth, newAgentIndex)[0] for action in legalActions]

    # random player uses average score and random action
    # max player uses max score and corresponding action
    if isRandomGhost:
      return float(sum(scores))/len(scores), random.choice(legalActions)
    else:
      maxScore = max(scores)
      return maxScore, legalActions[scores.index(maxScore)]


def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """

  # Useful information you can extract from a GameState (pacman.py) 
  pos = currentGameState.getPacmanPosition()
  ghostStates = currentGameState.getGhostStates()
  scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
  distanceMap = mypy.buildMazeDistanceMap(pos, currentGameState)
  
  # useful constants
  DISTANCE_WITHOUT_FARE = 4

  # Factor weights
  GHOST_DISTANCE_SCALE = -200;
  FOOD_DISTANCE_SCALE = 20;

  # Factor 1: ghost distance (ghostDistanceScore)
  #    (1) basic score is the reciprocal of min ghost distance
  #    (2) if min ghost distance is outside DISTANCE_WITHOUT_FARE, set score to 0
  #    (3) if agent is not scared about the ghost with min distance, flip the score
  ghostDists = [distanceMap[(int(ghost_x), int(ghost_y))] for ghost_x, ghost_y in currentGameState.getGhostPositions()]
  ghostDists_min = min(ghostDists) + 1  # plus one to avoid dividing by zero
  ghostDistanceScore = GHOST_DISTANCE_SCALE/ghostDists_min
  
  # if min ghost distance is larger than 3, no need to fare
  if ghostDists_min > DISTANCE_WITHOUT_FARE:
    ghostDistanceScore = 0

  # if the scared time of the ghost with min distance is nonzero, no need to fare
  ghostIdx = ghostDists.index(ghostDists_min-1)
  ghostDistanceScore = -ghostDistanceScore if scaredTimes[ghostIdx]!=0 else ghostDistanceScore
 

  # Factor 2: food distance (foodDistanceScore)
  #    (1) score is the reciprocal of min food distance
  hasFood = currentGameState.getFood()
  foodPos = []
  # find food positions
  for x in range(hasFood.width):
    for y in range(hasFood.height):
      if hasFood[x][y]:
        foodPos.append((x,y))
  # compute score as 1/min distance
  foodDists = [distanceMap[food_position] for food_position in foodPos]
  foodDists_min = min(foodDists) + 1 if len(foodDists)>0 else 1
  foodDistanceScore = FOOD_DISTANCE_SCALE/foodDists_min

  # Factor 3: food count
  #    (1) score is the reciprocal of food count
  foodCountScore = 1/(currentGameState.getNumFood()+1)

  # Factor 4: sum of scared time of ghosts
  scaredTimeScore = sum(scaredTimes)

  # Factor 5: score of state
  stateScore = currentGameState.getScore()

  scores = [foodDistanceScore, ghostDistanceScore, foodCountScore, scaredTimeScore, stateScore]
  weights = [1, -1, 0.1, 1, 1]

  return mypy.dotProduct(scores, weights)

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

