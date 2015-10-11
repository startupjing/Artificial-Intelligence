# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
from util import *

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]



def depthFirstSearch(problem):
    stack = Stack()
    visited = []
    startingState = problem.getStartState()
    stack.push(NodeObject(problem.getStartState(),None, "null" , 0))

    while stack:
        current_object = stack.pop()
       # print current_object

        current_state = current_object.state
        current_distance = current_object.cost


        if problem.isGoalState(current_state):
            return getActions(current_object)

        if(not(current_state in visited)):
            visited.append(current_state)

            for neighbor_triple in problem.getSuccessors(current_state):
                neighbor_state  = neighbor_triple[0]
                neighbor_parent = current_object
                neighbor_action = neighbor_triple[1]
                neighbor_cost = neighbor_triple[2] + current_distance
                neighbor_object = NodeObject(neighbor_state, neighbor_parent, neighbor_action, neighbor_cost)
                stack.push(neighbor_object)



def breadthFirstSearch(problem):

    queue = Queue()
    visited = []
    startingState = problem.getStartState()
    queue.push(NodeObject(problem.getStartState(),None, "null" , 0))

    while queue:
        current_object = queue.pop()
       # print current_object

        current_state = current_object.state
        current_distance = current_object.cost


        if problem.isGoalState(current_state):
            return getActions(current_object)
 
        if(not(current_state in visited)):
            visited.append(current_state)

            for neighbor_triple in problem.getSuccessors(current_state):
                neighbor_state  = neighbor_triple[0]
                neighbor_parent = current_object
                neighbor_action = neighbor_triple[1]
                neighbor_cost = neighbor_triple[2] + current_distance
                neighbor_object = NodeObject(neighbor_state, neighbor_parent, neighbor_action, neighbor_cost)
                queue.push(neighbor_object)


             

def uniformCostSearch(problem):

    pqueue = PriorityQueueWithFunction(priorityFunction)
    visited = []
    startingState = problem.getStartState()
    pqueue.push(NodeObject(problem.getStartState(),None, "null" , 0))

    while pqueue:
        current_object = pqueue.pop()
        #print current_object

        current_state = current_object.state
        current_distance = current_object.cost


        if problem.isGoalState(current_state):
            return getActions(current_object)

        if(not(current_state in visited)):
            visited.append(current_state)

            for neighbor_triple in problem.getSuccessors(current_state):
                neighbor_state  = neighbor_triple[0]
                neighbor_parent = current_object
                neighbor_action = neighbor_triple[1]
                neighbor_cost = neighbor_triple[2] + current_distance
                neighbor_object = NodeObject(neighbor_state, neighbor_parent, neighbor_action, neighbor_cost)
                pqueue.push(neighbor_object)



    
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):

    def costFunction(obj):
        return obj.cost + heuristic(obj.state, problem)

    pqueue = PriorityQueueWithFunction(costFunction)
    visited = []
    startingState = problem.getStartState()
    pqueue.push(NodeObject(problem.getStartState(),None, "null" , 0))

    while pqueue:
        current_object = pqueue.pop()
       # print current_object

        current_state = current_object.state
        current_distance = current_object.cost


        if problem.isGoalState(current_state):
            return getActions(current_object)

        if(not(current_state in visited)):
            visited.append(current_state)

            for neighbor_triple in problem.getSuccessors(current_state):
                neighbor_state  = neighbor_triple[0]
                neighbor_parent = current_object
                neighbor_action = neighbor_triple[1]
                neighbor_cost = neighbor_triple[2] + current_distance
                neighbor_object = NodeObject(neighbor_state, neighbor_parent, neighbor_action, neighbor_cost)
                pqueue.push(neighbor_object)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch



# Utility functions
def getActions(node):
    from game import Directions
    n = Directions.NORTH
    s = Directions.SOUTH
    e = Directions.EAST
    w = Directions.WEST

    dic = {'South':s, 'North':n, 'East':e, 'West':w }

    actions  = []
    actions_str = []
    parent = node.parent 

    while parent != None:
        actions.append(dic[node.action])
        actions_str.append(node.action)
        node = node.parent
        parent = node.parent
    
    actions.reverse()

    actions_str.reverse()
    #print actions_str

    return actions


def priorityFunction(node):
    return node.cost


# Utility class
class NodeObject(object):
    def __init__(self, state=None,parent=None, action=None, cost=None):
        self.parent = parent
        self.action = action
        self.state = state
        self.cost = cost

    def __str__(self):
        return "current state: " + str(self.state)


