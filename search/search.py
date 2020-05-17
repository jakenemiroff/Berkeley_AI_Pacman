# search.py
# ---------
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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    #define visited, which is a list containing all the visited nodes
    #define fringe, which is a stack containing the fringe
    visited = []
    fringe = util.Stack()
    fringe.push((problem.getStartState(), []))

    #while the fringe is not empty do the following:
    while not fringe.isEmpty():
        
        #pop off last node entered into the fringe
        #assign the first element of the node to state and the second element of the node to actions
        node = fringe.pop()
        state = node[0]
        actions = node[1]

        #check if the first node is the goal. If it is, return the associated actions
        if problem.isGoalState(state):
            return actions

        #if node has not been visited add it to the list of visited nodes and do the following:
        if state not in visited:

            visited.append(state)
            successorNodes = problem.getSuccessors(state)

            #loop through the successor nodes
            for nextNode in successorNodes:
                
                #assign the first element of the successor node to nextState and the second element of the successor node to nextAction 
                nextState = nextNode[0]
                nextAction = nextNode[1]

                #if not put it in the fringe
                if nextState not in visited:
                    fringe.push((nextState, actions + [nextAction]))

    util.raiseNotDefined()
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    #define visited, which is a list containing all the visited nodes
    #define fringe, which is a stack containing the fringe
    visited = []
    fringe = util.Queue()
    fringe.push((problem.getStartState(), []))

    #while the fringe is not empty do the following:
    while not fringe.isEmpty():
        
        #pop off last node entered into the fringe
        #assign the first element of the node to state and the second element of the node to actions
        node = fringe.pop()
        state = node[0]
        actions = node[1]

        #check if the first node is the goal. If it is, return the associated actions
        if problem.isGoalState(state):
            return actions

        #if node has not been visited add it to the list of visited nodes and do the following:
        if state not in visited:
            
            visited.append(state)

            successorNodes = problem.getSuccessors(state)

            #loop through the successor nodes
            for nextNode in successorNodes:
                
                #assign the first element of the successor node to nextState and the second element of the successor node to nextAction 
                nextState = nextNode[0]
                nextAction = nextNode[1]

                #if not put it in the fringe
                if nextState not in visited:
                    fringe.push((nextState, actions + [nextAction]))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    #define visited, which is a list containing all the visited nodes
    #define fringe, which is a stack containing the fringe
    fringe = util.PriorityQueue()
    fringe.push((problem.getStartState(), [], 0), 0)
    visited = []

    #while the fringe is not empty do the following:
    while not fringe.isEmpty():

        #pop off last node entered into the fringe
        #assign the first element of the node to state, the second element of the node to actions, and the third element of the node to cost
        node = fringe.pop()
        state = node[0]
        actions = node[1]
        cost = node[2]
        
        #check if the first node is the goal. If it is, return the associated actions
        if problem.isGoalState(state):
            return actions
        
        #if node has not been visited add it to the list of visited nodes and do the following:
        if state not in visited:
        
            visited.append(state)

            successorNodes = problem.getSuccessors(state)
        
            #loop through the successor nodes
            for nextNode in successorNodes:
                
                #assign the first element of the successor node to nextState, the second element of the successor node to nextAction,
                #and the third element of the successor node to nextCost 
                nextState = nextNode[0]
                nextAction = nextNode[1]
                nextCost = nextNode[2]
        
                #if the next state has not been visited get the cost and push that and the associated node into the fringe
                if nextState not in visited:
        
                    pathCost = cost + nextCost
                    fringe.push((nextState, actions + [nextAction], pathCost), pathCost)
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    #define visited, which is a list containing all the visited nodes
    #define fringe, which is a stack containing the fringe
    fringe = util.PriorityQueue()
    fringe.push((problem.getStartState(), [], 0), 0)
    visited = []

    #while the fringe is not empty do the following:
    while not fringe.isEmpty():

        #assign the first element of the successor node to nextState, the second element of the successor node to nextAction,
        #and the third element of the successor node to nextCost 
        node = fringe.pop()
        state = node[0]
        actions = node[1]
        cost = node[2]

        #check if the first node is the goal. If it is, return the associated actions        
        if problem.isGoalState(state):    
            return actions
        
        #if node has not been visited add it to the list of visited nodes and do the following:
        if state not in visited:
        
            visited.append(state)

            successorNodes = problem.getSuccessors(state)

            #loop through the successor nodes
            for nextNode in successorNodes:

                #assign the first element of the successor node to nextState, the second element of the successor node to nextAction,
                #and the third element of the successor node to nextCost                
                nextState = nextNode[0]
                nextAction = nextNode[1]
                nextCost = nextNode[2]

                #if the next state has not been visited get the cost using `heuristic` and push that and the associated node into the fringe
                if nextState not in visited:

                    pathCost = cost + nextCost
                    totalCost = pathCost + heuristic(nextState, problem)
                    fringe.push((nextState, actions + [nextAction], pathCost), totalCost)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
