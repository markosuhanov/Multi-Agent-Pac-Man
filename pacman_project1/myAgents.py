# myAgents.py
# ---------------
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


from searchProblems import PositionSearchProblem
from util import *
from game import Agent, Directions
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""


def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]


class MyAgent(Agent):

    states = []

    def initialize(self):
        self.maze_cleared = False
        self.agent_actions = []

    def getAction(self, state):
        if self.maze_cleared:
            return Directions.STOP
        elif not self.agent_actions:
            self.agent_actions = search.breadthFirstSearch(FoodProblem(state, self.index))
        if self.agent_actions:
            next_action = self.agent_actions[0]
            self.agent_actions.remove(next_action)
            return next_action
        else:
            self.maze_cleared = True
            return Directions.STOP

class FoodProblem(PositionSearchProblem):

    def __init__(self, gameState, agentIndex):

        self.agentIndex = agentIndex
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self.positions_of_food = gameState.getFood().asList()
        self.walls = gameState.getWalls()
        self._visited = {}
        self._visitedlist = []
        self._expanded = 0  # DO NOT CHANGE
        self.numOfAgents = gameState.getNumPacmanAgents()
        agent_food = len(self.positions_of_food) // self.numOfAgents + 1
        x_position = agentIndex * agent_food
        y_position = (agentIndex + 1) * agent_food
        self.foodByAgent = self.positions_of_food[x_position:y_position]

    def isGoalState(self, state):
        if len(self.positions_of_food) <= self.numOfAgents:
            return state in self.positions_of_food
        if state in self.positions_of_food:
            if (state not in MyAgent.states) and (state in self.foodByAgent):
                MyAgent.states.append(state)
                return True
            elif state not in MyAgent.states and manhattanDistance(state, self.startState) <= pow(1 + self.agentIndex, 2):
                MyAgent.states.append(state)
                return True
            else:
                return state in self.foodByAgent
        else:
            return False


class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):

        return search.aStarSearch(AnyFoodSearchProblem(gameState, self.index))

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited = {}
        self._visitedlist = []
        self._expanded = 0  # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        "*** YOUR CODE HERE ***"

        if (self.food[x][y]):
            return True
        return False

