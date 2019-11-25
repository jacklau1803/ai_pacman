import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core.distance import manhattan
from pacai.core.directions import Directions


class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best.
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        newPosition = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        distance = 0

        if newFood.count() == oldFood.count():
            distance = manhattan(newFood.asList()[0], newPosition)
            for pos in newFood.asList():
                if manhattan(pos, newPosition) < distance:
                    distance = manhattan(pos, newPosition)
        for ghost in newGhostStates:
            distance += 2 ** (2 - manhattan(ghost.getPosition(), newPosition))
        return 0 - distance


class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        self.evaluationFunction = MultiAgentSearchAgent.getEvaluationFunction(
            self)

    def getAction(self, gameState):
        return self.minimaxSearch(gameState, 1, 0)

    def minimaxSearch(self, gameState, depth, agentIndex):
        if depth > self.getTreeDepth() or gameState.isOver():
            return self.evaluationFunction(gameState)
        moves = [action for action in gameState.getLegalActions(
            agentIndex) if action != Directions.STOP]
        nextIndex = agentIndex + 1
        nextDepth = depth
        if nextIndex >= gameState.getNumAgents():
            nextIndex = 0
            nextDepth += 1
        minimax = [self.minimaxSearch(gameState.generateSuccessor(
            agentIndex, action), nextDepth, nextIndex) for action in moves]
        if depth == 1 and agentIndex == 0:
            possibleIndices = [index for index in range(
                len(minimax)) if minimax[index] == max(minimax)]
            return moves[random.choice(possibleIndices)]
        if agentIndex == 0:
            return max(minimax)
        else:
            return min(minimax)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        self.evaluationFunction = MultiAgentSearchAgent.getEvaluationFunction(
            self)

    def getAction(self, gameState):
        return self.alphaBeta(gameState, 1, 0, -float("inf"), float("inf"))

    def alphaBeta(self, gameState, depth, agentIndex, alpha, beta):
        if depth > self.getTreeDepth() or gameState.isOver():
            return self.evaluationFunction(gameState)
        moves = [action for action in gameState.getLegalActions(
            agentIndex) if action != Directions.STOP]
        nextIndex = agentIndex + 1
        nextDepth = depth
        if nextIndex >= gameState.getNumAgents():
            nextIndex = 0
            nextDepth += 1
        if depth == 1 and agentIndex == 0:
            ab = [self.alphaBeta(gameState.generateSuccessor(
                agentIndex, action), nextDepth, nextIndex, alpha, beta) for action in moves]
            possibleIndices = [index for index in range(
                len(ab)) if ab[index] == max(ab)]
            return moves[random.choice(possibleIndices)]
        if agentIndex == 0:
            result = -float("inf")
            for action in moves:
                result = max(result, self.alphaBeta(gameState.generateSuccessor(
                    agentIndex, action), nextDepth, nextIndex, alpha, beta))
                if result >= beta:
                    return result
                alpha = max(alpha, result)
            return result
        else:
            result = float("inf")
            for action in moves:
                result = min(result, self.alphaBeta(gameState.generateSuccessor(
                    agentIndex, action), nextDepth, nextIndex, alpha, beta))
                if result <= alpha:
                    return result
                beta = min(beta, result)
            return result


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)
        self.evaluationFunction = MultiAgentSearchAgent.getEvaluationFunction(
            self)

    def getAction(self, gameState):
        return self.expectimax(gameState, 1, 0)

    def expectimax(self, gameState, depth, agentIndex):
        if depth > self.getTreeDepth() or gameState.isOver():
            return self.evaluationFunction(gameState)
        moves = [action for action in gameState.getLegalActions(
            agentIndex) if action != Directions.STOP]
        nextIndex = agentIndex + 1
        nextDepth = depth
        if nextIndex >= gameState.getNumAgents():
            nextIndex = 0
            nextDepth += 1
        em = [self.expectimax(gameState.generateSuccessor(
            agentIndex, action), nextDepth, nextIndex) for action in moves]
        if depth == 1 and agentIndex == 0:
            possibleIndices = [index for index in range(
                len(em)) if em[index] == max(em)]
            return moves[random.choice(possibleIndices)]
        if agentIndex == 0:
            return max(em)
        else:
            return sum(em) / len(em)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: Calculate the sum of distances of foods and the distances of ghosts.
                 The threat is more important than food. Take the leftover penalty
                 into account. Minus them from the original score.

    """
    position = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    foodDist = 0
    for food in foods:
        foodDist += 2 * manhattan(position, food)
    ghostDist = 0
    for ghost in currentGameState.getGhostPositions():
        ghostDist += 4 * manhattan(position, ghost)
    penalty = -6 * len(food)
    return currentGameState.getScore() - foodDist - ghostDist + penalty


class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)
