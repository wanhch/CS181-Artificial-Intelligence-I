# logicPlan.py
# ------------
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


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    s1 = logic.to_cnf(A | B)
    s2 = ~A % (~B | C)
    s3 = logic.to_cnf(~A | ~B | C)
    return logic.conjoin(s1, s2, s3)
    util.raiseNotDefined()

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    D = logic.Expr('D')
    s1 = C % (B | D)
    s2 = A >> (~B & ~D)
    s3 = ~(B & ~C) >> A
    s4 = ~D >> C
    return logic.conjoin(s1, s2, s3, s4)
    util.raiseNotDefined()

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    WL0 = logic.PropSymbolExpr('WumpusAlive', 0)
    WL1 = logic.PropSymbolExpr('WumpusAlive', 1)
    WB0 = logic.PropSymbolExpr('WumpusBorn', 0)
    WK0 = logic.PropSymbolExpr('WumpusKilled', 0)
    s1 = WL1 % (WL0 & ~WK0 |(~WL0 & WB0))
    s2 = ~(WL0 & WB0)
    s3 = WB0
    return logic.conjoin(s1, s2, s3)
    util.raiseNotDefined()

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    cnf = logic.to_cnf(sentence)
    return logic.pycoSAT(cnf)
    util.raiseNotDefined()

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.associate('|', literals)
    util.raiseNotDefined()


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    s_list = []
    for i in literals:
        for j in literals:
            if i is not j:
                s_list.append((~i | ~j))
    return logic.conjoin(s_list)
    util.raiseNotDefined()


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    if len(literals) > 1:
        return atMostOne(literals) & atLeastOne(literals)
    else:
        return atLeastOne(literals)
    util.raiseNotDefined()


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    action_list = []
    keys = list(model.keys())
    for key in keys:
        if model[key] and (logic.PropSymbolExpr.parseExpr(key)[0] in actions):
            action_list.append(logic.PropSymbolExpr.parseExpr(key))
    action_list.sort(key=lambda action: int(action[1]))
    return [action[0] for action in action_list]
    util.raiseNotDefined()


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    successor_list = []
    if 0 <= x - 1 < walls_grid.width and 0 <= y < walls_grid.height:
        if not walls_grid.data[x - 1][y]:
            location = logic.PropSymbolExpr('P', x - 1, y, t - 1)
            action = logic.PropSymbolExpr('East', t - 1)
            successor_list.append(location & action)
    if 0 <= x + 1 < walls_grid.width and 0 <= y < walls_grid.height:
        if not walls_grid.data[x + 1][y]:
            location = logic.PropSymbolExpr('P', x + 1, y, t - 1)
            action = logic.PropSymbolExpr('West', t - 1)
            successor_list.append(location & action)
    if 0 <= x < walls_grid.width and 0 <= y - 1 < walls_grid.height:
        if not walls_grid.data[x][y - 1]:
            location = logic.PropSymbolExpr('P', x, y - 1, t - 1)
            action = logic.PropSymbolExpr('North', t - 1)
            successor_list.append(location & action)
    if 0 <= x < walls_grid.width and 0 <= y + 1 < walls_grid.height:
        if not walls_grid.data[x][y + 1]:
            location = logic.PropSymbolExpr('P', x, y + 1, t - 1)
            action = logic.PropSymbolExpr('South', t - 1)
            successor_list.append(location & action)
    return logic.PropSymbolExpr('P', x, y, t) % logic.associate('|', successor_list)


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    actions = ['North', 'South', 'East', 'West']
    (goal_x, goal_y) = problem.getGoalState()
    successor = []
    action = []
    start_sentence_temp = []
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            if (x, y) == problem.getStartState():
                start_sentence_temp.append(logic.PropSymbolExpr('P', x, y, 0))
            else:
                start_sentence_temp.append(logic.Expr("~", logic.PropSymbolExpr('P', x, y, 0)))
    start_sentence = [logic.conjoin(start_sentence_temp)]
    for t in range(0, 51):
        goal_sentence = [logic.PropSymbolExpr('P', goal_x, goal_y, t)]
        if t == 0:
            model = findModel(logic.conjoin(start_sentence + goal_sentence))
        else:
            action_propsymbolexpr = []
            successor_temp = []
            for x in range(1, width + 1):
                for y in range(1, height + 1):
                    if not walls[x][y]:
                        successor_temp = successor_temp + [pacmanSuccessorStateAxioms(x, y, t, walls)]
            successor.append(logic.conjoin(successor_temp))
            for act in actions:
                action_propsymbolexpr.append(logic.PropSymbolExpr(act, t - 1))
            action.append(exactlyOne(action_propsymbolexpr))
            print
            model = findModel(logic.conjoin(start_sentence + goal_sentence + action + successor))
        if model is not False:
            return extractActionSequence(model, actions)
    util.raiseNotDefined()



def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    actions = ['North', 'South', 'East', 'West']
    food = problem.startingGameState.data.food
    food_xy = []
    food_propsymbolexpr = []
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            if food[x][y]:
                food_xy.append((x, y))
    successor = []
    action = []
    start_sentence_temp = []
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            if (x, y) == problem.getStartState()[0]:
                start_sentence_temp.append(logic.PropSymbolExpr('P', x, y, 0))
            else:
                start_sentence_temp.append(logic.Expr("~", logic.PropSymbolExpr('P', x, y, 0)))
    start_sentence = [logic.conjoin(start_sentence_temp)]
    for t in range(0, 51):
        for i in range(len(food_xy)):
            (x, y) = food_xy[i]
            if t == 0:
                food_propsymbolexpr.append([logic.PropSymbolExpr('P', x, y, t)])
            else:
                food_propsymbolexpr[i].append(logic.PropSymbolExpr('P', x, y, t))
        food_sentence = []
        for i in range(len(food_propsymbolexpr)):
            food_sentence.append(atLeastOne(food_propsymbolexpr[i]))
        if t == 0:
            model = findModel(logic.conjoin(start_sentence + food_sentence))
        else:
            action_propsymbolexpr = []
            successor_temp = []
            for x in range(1, width + 1):
                for y in range(1, height + 1):
                    if not walls[x][y]:
                        successor_temp = successor_temp + [pacmanSuccessorStateAxioms(x, y, t, walls)]
            successor.append(logic.conjoin(successor_temp))
            for act in actions:
                action_propsymbolexpr.append(logic.PropSymbolExpr(act, t - 1))
            action.append(exactlyOne(action_propsymbolexpr))
            model = findModel(logic.conjoin(start_sentence + action + successor + food_sentence))
        if model is not False:
            return extractActionSequence(model, actions)
    util.raiseNotDefined() 

# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    