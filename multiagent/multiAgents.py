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


import random

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        "*** YOUR CODE HERE ***"

        #initialize foodDistance, could be any number except for 0 due to a potential division by 0 error
        foodDistance = 1

        #find manhattanDistance for pacman's new position and the remaining food
        for food in newFood.asList():
            foodDistance = manhattanDistance(newPos, food)

        #find manhattanDistance between pacman's new position and the position of the ghosts
        #if the ghost is close (distance less than 2), return a value of -1 to indicate that the move is not a good option
        for ghost in newGhostStates:
            if (manhattanDistance(newPos, ghost.getPosition()) < 2):
                return -1

        #return the value of the gamee score with the successor action + a reciprocal of the distance to the remaining food
        return successorGameState.getScore() + 1 / foodDistance


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

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
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

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        num_of_agents = gameState.getNumAgents()

        depth = self.depth * num_of_agents

        self.minimax(gameState, depth, num_of_agents)

        return self.action

	# New function defined to recursively traverse the minimax tree
    def minimax(self, gameState, depth, num_of_agents):

        if (gameState.isWin() or gameState.isLose() or depth <= 0):
            return self.evaluationFunction(gameState)

        # if depth is greater than or equal to 1
        else:
            agentIndex = 0
            maximumValues = []
            minimumValues = []

            if (depth % num_of_agents != 0):
                agentIndex = num_of_agents - (depth % num_of_agents)

            actions = gameState.getLegalActions(agentIndex)

            for action in actions:

                successorGameState = gameState.generateSuccessor(agentIndex, action)

                if (agentIndex == 0): #pacman agent

                    #store max value from recursive call with the associated action in a tuple
                    maximumValueTuple = (self.minimax(successorGameState, depth - 1, num_of_agents), action)

                    maximumValues.append(maximumValueTuple)


                else: #ghost agents

                    #store min value from recursive call with the associated action in a tuple
                    minimumValueTuple = (self.minimax(successorGameState, depth - 1, num_of_agents), action)

                    minimumValues.append(minimumValueTuple)


            if (agentIndex == 0):
                self.action = max(maximumValues)[1]	#store the action associated with max value (second part stored in tuple)
                return max(maximumValues)[0] #return max value (first part stored in tuple)

            else:
                return min(minimumValues)[0] #return min value (first part stored in tuple)



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


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

        num_of_agents = gameState.getNumAgents()

        depth = self.depth * num_of_agents

        self.expectimax(gameState, depth, num_of_agents)

        return self.action

	# New function defined to recursively traverse the minimax tree
    def expectimax(self, gameState, depth, num_of_agents):

        if (gameState.isWin() or gameState.isLose() or depth <= 0):
            return self.evaluationFunction(gameState)


        # if depth is greater than or equal to 1
        else:
            agentIndex = 0
            maximumValues = []
            chanceValues = []

            if (depth % num_of_agents != 0):
                agentIndex = num_of_agents - (depth % num_of_agents)

            actions = gameState.getLegalActions(agentIndex)

            for action in actions:

                successorGameState = gameState.generateSuccessor(agentIndex, action)

                if (agentIndex == 0): #pacman agent

                    #store max value from recursive call with the associated action in a tuple
                    maximumValueTuple = (self.expectimax(successorGameState, depth - 1, num_of_agents), action)

                    maximumValues.append(maximumValueTuple)


                else: #ghost agents

                    #store chance value from recursive call with the associated action in a tuple
                    chanceValueTuple = (self.expectimax(successorGameState, depth - 1, num_of_agents), action)

                    chanceValues.append(chanceValueTuple)


                    averageValue = 0
                    averageValueMove = 0

                    #calculate the average of all chance nodes
                    for value in chanceValues:
                        averageValue += chanceValues[chanceValues.index(value)][0]

                    averageValue = averageValue / len(chanceValues)
                    averageValueMove = averageValue


            if (agentIndex == 0):
                self.action = max(maximumValues)[1]	#store the action associated with max value (second part stored in tuple)
                return max(maximumValues)[0] #return max value (first part stored in tuple)

            else:
                return averageValueMove #return average value from all ghost moves


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
