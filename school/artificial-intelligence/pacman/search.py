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

def depthFirstSearch(problem: SearchProblem):
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
    # DFS uses a LIFO stack. We set up our frontier by instantiating and
    # assigning the stack to it.
    frontier = util.Stack()

    # We have to figure out where to start so we get the start state.
    startState = problem.getStartState()

    # It's not enough to just push the state on to our stack because we don't have
    # the tree visually in front of us to look at. So we must push a pair that has
    # the state and the path to get there. When we eventually get to the goal then
    # whatever path we have currently will be the answer path.
    startPath = []
    frontier.push((startState, startPath))

    # We use a set to track the states where we've been because we only care
    # about have we ever expanded these states before.
    visited = set()

    # We keep lopping as long as there are more to explore. If the frontier becomes
    # empty and we haven't hit the goal then there is no solution.
    while not frontier.isEmpty():
        # Pop the next pair node to expand.
        currentState, pathSoFar = frontier.pop()

        # We have to ask if we've already expanded this state before.
        # If we have then we skip it and go pop the next one.
        if currentState in visited:
            continue

        # At expansion time we mark this state as visited.
        visited.add(currentState)

        # Check if we've reached the goal. This goal check happens
        # at expansion time. 
        if problem.isGoalState(currentState):
            return pathSoFar

        # Coming here means we haven't reach the goal. So we generate
        # the successors and push them on to the frontier.
        successors = problem.getSuccessors(currentState)

        for successorState, action, stepCost in successors:
            # Only pushing the successor state if we haven't already expanded it.
            # This is done because we don't want to fill the stack with unnecessary states.
            if successorState not in visited:
                # We build a new path by specifically creating a new list.
                # Having a new list is critical because each frontier entry 
                # must have its own independent path.
                newPath = pathSoFar + [action]
                frontier.push((successorState, newPath))

    # If we reach here then there is no solution. 
    return None

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
