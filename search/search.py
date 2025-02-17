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
from game import Directions
from typing import List

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

def visited_check( explored_set , goal ):
    for pair in explored_set:
        if pair[0] == goal:
            return pair
    return False

def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
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

    frontier = util.Stack()
    frontier.push( (problem.getStartState() , []) )
    explored_set = set()

    # frontier consists of tuples containing a state and a string of directions
    # this way we can add an extra step in directions by just "adding" a string to another

    while not frontier.isEmpty():

        node = frontier.pop()

        if problem.isGoalState(node[0]):    # node[0] : state of node
            return node[1]  # node[1] : string consisting of the path to goal
        
        if not (node[0] in explored_set):

            explored_set.add(node[0])

            for child in problem.getSuccessors(node[0]):
                # when adding a child in frontier the new directions derive from just the 
                # addition of the directions of the parent node + the single step of the child
                frontier.push((child[0] , (node[1] + [child[1]])))

    return None
 
def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # exactly the same comments for this application as with the dfs algorithm
    # the only difference between the two is that frontier is a Queue instead of a Stack

    frontier = util.Queue()
    frontier.push( (problem.getStartState() , []) )
    explored_set = set()

    while not frontier.isEmpty():

        node = frontier.pop()

        if problem.isGoalState(node[0]):    # node[0] : state of node
            return node[1]  # node[1] : string consisting of the path to goal
        
        if not (node[0] in explored_set):

            explored_set.add(node[0])
            
            for child in problem.getSuccessors(node[0]):
                # when adding a child in frontier the new directions derive from just the 
                # addition of the directions of the parent node + the single step of the child
                frontier.push( ( child[0] , ( node[1] + [ child[1] ] ) ) )

    return None

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    frontier = util.PriorityQueue()
    frontier.push( ( problem.getStartState() , [])  , 0 )
    explored_set = set()

    # tuples now consist of one elements : a tuple containing state and a string of directions 
    # frontier is now a PQueue and each element is sorted based on the minimum cost required
    # to get to the node

    while not frontier.isEmpty():

        node = frontier.pop()

        if problem.isGoalState( node[0] ):  # node[0] : state of node
            return node[1] # node[1] : string consisting of the path to goal
        
        if  not (node[0] in explored_set):

            explored_set.add( node[0]  )

            for succesor in problem.getSuccessors(node[0]):
                
                child = succesor[0] 
                # child is the new state created by the action on the parent

                frontier.update( ( child , (node[1] + [succesor[1]]) ), problem.getCostOfActions( (node[1] + [succesor[1]]) ) ) 
                # the cost of a new node is the cost of the parent plus the cost of action 
    return None 

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:

    frontier = util.PriorityQueue()
    frontier.push( ( problem.getStartState() , [] , 0 )  , heuristic(  problem.getStartState() , problem) )
    explored_set = set()

    # elements of frontier consist again of a tuple of 3 elements just like ucs 
    # we are using again a PQueue for frontier. The nodes in frontier are sorted by 
    # the sum of the true cost required to get to node plus the heuristic cost



    while not frontier.isEmpty():

        node = frontier.pop()

        if problem.isGoalState( node[0] ):  # node[0] : state of node
            return node[1]  # node[1] : string consisting of the path to goal
        
        result = visited_check(explored_set , node[0])

        # visited_check searches if the state of the current node has been visited
        # if it's found it returns the tuple of the node , else it returns False

        if result == False:

            explored_set.add( (node[0] , node[2]) )
            # in explored set we store tuples containing the state and the minimum
            # real cost we have found at the moment

            for succesor in problem.getSuccessors(node[0]):

                child = succesor[0]
                result = visited_check(explored_set , child)
                g_cost = problem.getCostOfActions( (node[1] + [succesor[1]]) )
                total_cost = g_cost + heuristic( child, problem)

                if result == False:
                    # if the new child node has not been visited, calculate the costs and 
                    # we add it to the frontier
                    g_cost = problem.getCostOfActions( (node[1] + [succesor[1]]) )
                    total_cost = g_cost + heuristic( child, problem)
                    frontier.update( ( child , (node[1] + [succesor[1]]) , g_cost), total_cost )  
                else:
                    # if the exact state has already been expanded at some other point 
                    # but now we have found a path with lower cost we update the frontier
                    # and remove the node from the visited set
                    if result[1] > g_cost:
                        frontier.update( ( child , (node[1] + [succesor[1]]) , g_cost), total_cost )  
                        explored_set.remove(result)
      
    return None 

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
