# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter()   # state values
    self.qValues = util.Counter()  # state Q-values
     
    "*** YOUR CODE HERE ***"

    # useful information
    all_states = self.mdp.getStates()

    for i in range(0, self.iterations):
      state_values = util.Counter()

      for state in all_states:
        actions = self.mdp.getPossibleActions(state)
        max_qValue = float('-Inf')

        # terminal state or no possible actions
        if self.mdp.isTerminal(state) or not actions:
          state_values[state] = 0
          continue
        else:

          for action in actions:
            transitions = self.mdp.getTransitionStatesAndProbs(state, action)

            # compute q-value for (state, action) pair
            qValue = 0
            for t in transitions:
              qValue += t[1] * (self.mdp.getReward(state, action, t[0]) + self.discount * self.values[t[0]])
            self.qValues[(state, action)] = qValue

            # update max q-value
            max_qValue = max(max_qValue, qValue)

          state_values[state] = max_qValue

      self.values = state_values


    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    return self.qValues[(state, action)]
    

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"

    # useful information
    possible_actions = self.mdp.getPossibleActions(state)

    # terminal state or no possible actions for this state
    if self.mdp.isTerminal(state) or not possible_actions:
      return None

    best_action = None
    maxValue = float('-Inf')
    
    # choose the action with max q-value
    for action in possible_actions:
      if self.qValues[(state, action)] > maxValue:
        maxValue = self.qValues[(state, action)]
        best_action = action

    return best_action


  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
