# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    fifo_queue = util.Stack(); # initialize the stack
    explored = set();
    fifo_queue.push((problem.getStartState(),[],0));# push current state onto the stack as well as empty direction list, and 0 cost

    while not fifo_queue.isEmpty(): # while queue is not empty
        curState, curMoves, curCost = fifo_queue.pop(); # pop off the stuff off the stack

        if(curState in explored):
            continue;

        explored.add(curState);

        if problem.isGoalState(curState):
            return curMoves;

        for state, direction, cost in problem.getSuccessors(curState):
            fifo_queue.push((state, curMoves+[direction], curCost));
    return [];


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    fifo_queue = util.Queue(); # initialize the queue
    explored = set();
    fifo_queue.push((problem.getStartState(),[],0));# init: push current state onto the stack as well as empty direction list, and 0 cost

    while not fifo_queue.isEmpty(): # while queue is not empty
        curState, curMoves, curCost = fifo_queue.pop(); # pop off the stuff off the stack

        if(curState in explored): # if current state in explored then continue
            continue;

        explored.add(curState); # if not, add it to explored

        if problem.isGoalState(curState): # if goal state, return move list
            return curMoves;

        for state, direction, cost in problem.getSuccessors(curState): # else get successors and push them on the stack
            fifo_queue.push((state, curMoves+[direction], curCost));
    return []; # if nothing found, return null list

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    priorityQueue = util.PriorityQueue(); # initialize the priority queue
    explored = set();
    priorityQueue.push((problem.getStartState(),[],0), 0);# init: push current state onto the stack as well as empty direction list, and 0 cost

    while not priorityQueue.isEmpty(): # while queue is not empty
        curState, curMoves, curCost = priorityQueue.pop(); # pop off the stuff off the stack

        if(curState in explored): # if current state in explored then continue
            continue;

        explored.add(curState); # if not, add it to explored

        if problem.isGoalState(curState): # if goal state, return move list
            return curMoves;

        for state, direction, cost in problem.getSuccessors(curState): # else get successors and push them on the stack
            newMoves = curMoves + [direction]
            priorityQueue.push((state, curMoves+[direction], curCost), problem.getCostOfActions(newMoves)); # push onto priority queue with new move cost (current moves + direction you are going)
    return []; # if nothing found, return null list

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    priorityQueue = util.PriorityQueue(); # initialize the priority queue
    explored = set();
    priorityQueue.push((problem.getStartState(),[],0), 0);# init: push current state onto the stack as well as empty direction list, and 0 cost

    while not priorityQueue.isEmpty(): # while queue is not empty
        curState, curMoves, curCost = priorityQueue.pop(); # pop off the stuff off the stack

        if(curState in explored): # if current state in explored then continue
            continue;

        explored.add(curState); # if not, add it to explored

        if problem.isGoalState(curState): # if goal state, return move list
            return curMoves;

        for state, direction, cost in problem.getSuccessors(curState): # else get successors and push them on the stack
            newMoves = curMoves + [direction]
            costWithHeuristic = problem.getCostOfActions(newMoves) + heuristic(state, problem)
            priorityQueue.push((state, curMoves+[direction], curCost), costWithHeuristic); # push onto priority queue with new move cost (things on frontier + heuristic)
    return []; # if nothing found, return null list


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
