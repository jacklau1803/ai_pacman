"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""
from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    fringe = Stack()
    visited = list()
    fringe.push((problem.startingState(), ()))
    while not fringe.isEmpty():
        curr = fringe.pop()
        if problem.isGoal(curr[0]):
            return list(curr[1])
        if not curr[0] in visited:
            visited.append(curr[0])
            nextSteps = problem.successorStates(curr[0])
            for i in nextSteps:
                path = list(curr[1])
                path.append(i[1])
                next = (i[0], tuple(path))
                if not i[0] in visited:
                    fringe.push(next)
    return None


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    fringe = Queue()
    visited = list()
    fringe.push((problem.startingState(), ()))
    while not fringe.isEmpty():
        curr = fringe.pop()
        if problem.isGoal(curr[0]):
            return list(curr[1])
        if not curr[0] in visited:
            visited.append(curr[0])
            nextSteps = problem.successorStates(curr[0])
            for i in nextSteps:
                path = list(curr[1])
                path.append(i[1])
                next = (i[0], tuple(path))
                if not i[0] in visited:
                    fringe.push(next)
    return None


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    fringe = PriorityQueue()
    visited = list()
    fringe.push((problem.startingState(), None, None, list()), 0)
    while not fringe.isEmpty():
        curr = fringe.pop()
        if problem.isGoal(curr[0]):
            return curr[3]
        if not curr[0] in visited:
            visited.append(curr[0])
            nextSteps = problem.successorStates(curr[0])
            for i in nextSteps:
                if not i[0] in visited:
                    path = list(curr[3])
                    path.append(i[1])
                    fringe.push((i[0], i[1], i[2], path),
                                problem.actionsCost(path))
    return None


def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    fringe = PriorityQueue()
    visited = list()
    fringe.push((problem.startingState(), ()),
                heuristic(problem.startingState(), problem))
    while not fringe.isEmpty():
        curr = fringe.pop()
        if problem.isGoal(curr[0]):
            return list(curr[1])
        if not curr[0] in visited:
            visited.append(curr[0])
            nextSteps = problem.successorStates(curr[0])
            for i in nextSteps:
                path = list(curr[1])
                path.append(i[1])
                next = (i[0], tuple(path))
                if not i[0] in visited:
                    path = list(curr[1])
                    path.append(i[1])
                    fringe.push(next, problem.actionsCost(
                        path) + heuristic(i[0], problem))
    return None
