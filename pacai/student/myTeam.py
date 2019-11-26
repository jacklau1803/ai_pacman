import random
from pacai.util import reflection
from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.util import counter
from pacai.core.directions import Directions


def createTeam(firstIndex, secondIndex, isRed,
               first='pacai.student.myTeam.DefensiveReflexAgent',
               second='pacai.student.myTeam.AlphaBetaAgent'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = reflection.qualifiedImport(first)
    secondAgent = reflection.qualifiedImport(second)

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]


class DefensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that tries to keep its side Pacman-free.
    This is to give you an idea of what a defensive agent could be like.
    It is not the best or only way to make such an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = counter.Counter()
        successor = self.getSuccessor(gameState, action)

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i)
                   for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman(
        ) and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if (len(invaders) > 0):
            dists = [self.getMazeDistance(
                myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(
            self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -10,
            'stop': -100,
            'reverse': -2
        }


class OffensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food.
    This agent will give you an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = counter.Counter()
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food)
                               for food in foodList])
            features['distanceToFood'] = minDistance
        return features

    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': -1
        }


class AlphaBetaAgent(ReflexCaptureAgent):

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getAction(self, state):
        result = self.AlphaBeta(state, 2, self.index,
                                float('-inf'), float('inf'))[1]
        if result == 'Stop':
            c = random.choice(state.getLegalActions(self.index))
            return c
        else:
            return result

    def AlphaBeta(self, state, depth, agent, alpha, beta):
        if agent == state.getNumAgents():
            depth -= 1
            agent = 0
        if state.isOver() or depth == 0:
            val_act = [self.evaluationFunction(state), None]
            return val_act
        if agent == 0:
            val_act = [float('-inf'), None]
            for action in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, action)
                score = self.AlphaBeta(
                    successor, depth, agent + 1, alpha, beta)
                if val_act[0] < score[0]:
                    val_act = [score[0], action]
                if val_act[0] >= beta:
                    return val_act
                alpha = max(alpha, score[0])
        else:
            val_act = [float('inf'), None]
            for action in state.getLegalActions(agent):
                successor = state.generateSuccessor(agent, action)
                score = self.AlphaBeta(
                    successor, depth, agent + 1, alpha, beta)
                if val_act[0] > score[0]:
                    val_act = [score[0], action]
                if val_act[0] <= alpha:
                    return val_act
                beta = min(beta, score[0])
        return val_act

    def evaluationFunction(self, state):
        if state.isOnBlueTeam(self.index):
            foods = state.getRedFood().asList()
            pos = state.getAgentPosition(self.index)
            # caps = state.getRedCapsules()
            # ghosts = [state.getAgentPosition(x)
            #           for x in state.getRedTeamIndices()]
            # g_dis = 0
            f_dis = float('inf')
            # c_dis = float('inf')
            # g_dis = min([self.getMazeDistance(pos, ghost)
            #              for ghost in ghosts])
            f_dis = min([self.getMazeDistance(pos, food) for food in foods])
            # c_dis = min([self.getMazeDistance(pos, capsule)
            #              for capsule in caps])
            # if g_dis == 0:
            #     g_dis += 1
            score = f_dis
        else:
            foods = state.getBlueFood().asList()
            pos = state.getAgentPosition(self.index)
            # caps = state.getBlueCapsules()
            # ghosts = [state.getAgentPosition(x)
            #           for x in state.getBlueTeamIndices()]
            # g_dis = 0
            f_dis = float('inf')
            # c_dis = float('inf')
            # g_dis = min([self.getMazeDistance(pos, ghost)
            #              for ghost in ghosts])
            f_dis = min([self.getMazeDistance(pos, food) for food in foods])
            # c_dis = min([self.getMazeDistance(pos, capsule)
            #              for capsule in caps])
            # if g_dis == 0:
            #     g_dis += 1
            score = f_dis
        # p = currentGameState.getAgentPosition(self.index)
        # foods = currentGameState.getFood().asList()
        # capsules = currentGameState.getCapsules()
        # ghostStates = currentGameState.getAgentPosition(self.index)
        # gp = [ghost.getPosition() for ghost in ghostStates]
        # scaredTimes = [ghost.getScaredTimer() for ghost in ghostStates]
        # g_dis = 0
        # f_dis = float('inf')
        # c_dis = float('inf')
        # h_dis = float('inf')
        # for food in foods:
        #     f_dis = min(f_dis, manhattan(p, food))
        # for capsule in capsules:
        #     c_dis = min(c_dis, manhattan(p, capsule))
        # for i in range(len(scaredTimes)):
        #     if scaredTimes[i] > 0:
        #         h_dis = min(h_dis, manhattan(p, gp[i]))
        #     else:
        #         g_dis += manhattan(p, gp[i])
        # if g_dis == 0:
        #     g_dis += 1
        # score = currentGameState.getScore() + 1 / f_dis + 1 / \
        #     h_dis + 1 / c_dis - 1 / g_dis
        return score
