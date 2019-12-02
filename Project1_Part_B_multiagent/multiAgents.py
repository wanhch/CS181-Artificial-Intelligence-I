# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        return successorGameState.getScore()

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
    Your minimax agent (question 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        agents_number = gameState.getNumAgents()
        action_value = []
        def without_stop(actions):
            return [action for action in actions if action != "Stop"]
        actions = without_stop(gameState.getLegalActions(0))
        def minimax_value(agentIndex, state, depth):
            if agentIndex == 0:
                depth = depth - 1
            if depth == -1 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            next_agentIndex = agentIndex + 1
            if next_agentIndex >= agents_number:
                next_agentIndex = 0
            state_list = []
            for legal_action in without_stop(state.getLegalActions(agentIndex)):
                state_list.append(state.generateSuccessor(agentIndex, legal_action))
            if depth == self.depth - 1 and agentIndex == 0:
                for state in state_list:
                    action_value.append(minimax_value(next_agentIndex, state, depth))
                return 0
            else:
                if agentIndex == 0:
                    value = max(minimax_value(next_agentIndex, state, depth) for state in state_list)
                else:
                    value = min(minimax_value(next_agentIndex, state, depth) for state in state_list)
                return value
        value = minimax_value(0, gameState, self.depth)
        return actions[action_value.index(max(action_value))]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        agents_number = gameState.getNumAgents()
        action_value = []
        def without_stop(actions):
            return [action for action in actions if action != "Stop"]
        actions = without_stop(gameState.getLegalActions(0))
        def minimax_value(agentIndex, state, depth, alpha, beta):
            if agentIndex == 0:
                depth = depth - 1
            if depth == -1 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            next_agentIndex = agentIndex + 1
            if next_agentIndex >= agents_number:
                next_agentIndex = 0
            action_list = without_stop(state.getLegalActions(agentIndex))
            if depth == self.depth - 1 and agentIndex == 0:
                for action in action_list:
                    next_state = state.generateSuccessor(agentIndex, action)
                    value = minimax_value(next_agentIndex, next_state, depth, alpha, beta)
                    alpha = max(alpha, value)
                    action_value.append(value)
                return 0
            else:
                if agentIndex == 0:
                    value = -1e18
                    for action in action_list:
                        next_state = state.generateSuccessor(agentIndex, action)
                        value = max(value, minimax_value(next_agentIndex, next_state, depth, alpha, beta))
                        if value > beta:
                            return value
                        alpha = max(alpha, value)
                else:
                    value = 1e18
                    for action in action_list:
                        next_state = state.generateSuccessor(agentIndex, action)
                        value = min(value, minimax_value(next_agentIndex, next_state, depth, alpha, beta))
                        if value < alpha:
                            return value
                        beta = min(beta, value)
                return value
        value = minimax_value(0, gameState, self.depth, -1e18, 1e18)
        return actions[action_value.index(max(action_value))]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        agents_number = gameState.getNumAgents()
        action_value = []
        def without_stop(actions):
            return [action for action in actions if action != "Stop"]
        actions = without_stop(gameState.getLegalActions(0))
        def minimax_value(agentIndex, state, depth):
            if agentIndex == 0:
                depth = depth - 1
            if depth == -1 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            next_agentIndex = agentIndex + 1
            if next_agentIndex >= agents_number:
                next_agentIndex = 0
            state_list = []
            for legal_action in without_stop(state.getLegalActions(agentIndex)):
                state_list.append(state.generateSuccessor(agentIndex, legal_action))
            if depth == self.depth - 1 and agentIndex == 0:
                for state in state_list:
                    action_value.append(minimax_value(next_agentIndex, state, depth))
                return 0
            else:
                value = 0.0
                if agentIndex == 0:
                    value = max(minimax_value(next_agentIndex, state, depth) for state in state_list)
                else:
                    for state in state_list:
                        value = value + minimax_value(next_agentIndex, state, depth)
                    value = value / len(state_list)
                return value
        value = minimax_value(0, gameState, self.depth)
        return actions[action_value.index(max(action_value))]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    value = currentGameState.getScore()
    posi = currentGameState.getPacmanPosition()
    def food_value(state):
        food_list = state.getFood().asList()
        if food_list:
            return max(1.0 / manhattanDistance(posi, food) for food in food_list)
        return 0

    def capsule_value(state):
        capsule_list = state.getCapsules()
        if capsule_list:
            return max(1.0 / manhattanDistance(posi, capsule) for capsule in capsule_list)
        return 0

    def ghost_value(state):
        value = 0
        ghost_list = state.getGhostStates()
        for ghost in ghost_list:
            distance = manhattanDistance(ghost.getPosition(), posi) + 1
            if ghost.scaredTimer > 0:
                value = value + 1.0 / distance
            else:
                value = value - 1.0 / distance
            if distance > 4:
                value = 0
        return value

    return value + food_value(currentGameState) + capsule_value(currentGameState) + ghost_value(currentGameState)
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
