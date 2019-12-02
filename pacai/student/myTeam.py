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

    def getFeatures(self, state, action):
        features = counter.Counter()
        successor = self.getSuccessor(state, action)

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

        rev = Directions.REVERSE[state.getAgentState(
            self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        return features

    def getWeights(self, state, action):
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

    def getFeatures(self, state, action):
        features = counter.Counter()
        successor = self.getSuccessor(state, action)
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

    def getWeights(self, state, action):
        return {
            'successorScore': 100,
            'distanceToFood': -1
        }


class AlphaBetaAgent(ReflexCaptureAgent):

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def evaluationFunction(self, state):
        if state.isOnBlueTeam(3):
            foods = state.getRedFood().asList()
            pos = state.getAgentPosition(3)
            ghosts = [state.getAgentPosition(x)
                      for x in state.getRedTeamIndices()]
            g_dis = float('inf')
            f_dis = 0
            for ghost in ghosts:
                g_dis += self.getMazeDistance(pos, ghost)
            for food in foods:
                f_dis += self.getMazeDistance(pos, food)
            nf = min([self.getMazeDistance(pos, food) for food in foods])
            score = 1 / nf - len(foods)
        else:
            foods = state.getBlueFood().asList()
            pos = state.getAgentPosition(self.index)
            ghosts = [state.getAgentPosition(x)
                      for x in state.getBlueTeamIndices()]
            g_dis = float('inf')
            f_dis = 0
            for ghost in ghosts:
                g_dis += self.getMazeDistance(pos, ghost)
            for food in foods:
                f_dis += self.getMazeDistance(pos, food)
            nf = min([self.getMazeDistance(pos, food) for food in foods])
            score = 0
        return score

    def getAction(self, state):
        action = self.minimaxDecision(state, 1, self.index, self.index, 0)[1]
        return action

    def minimaxDecision(self, state, depth, agent, init, count):
        if agent == init and count != 0:
            depth -= 1
        if agent == 4:
            agent = 0
        elif agent == 5:
            agent = 1
        if state.isOver() or depth == 0:
            return (self.evaluationFunction(state), Directions.STOP)
        actions = [action for action in state.getLegalActions(
            agent) if action != Directions.STOP]
        if agent == init:
            minimax = [(self.minimaxDecision(state.generateSuccessor(
                agent, action), depth, agent + 1, init, count + 1)[0], action) for action in actions]
            minimax.sort(key=lambda tup: tup[0], reverse=True)
            return minimax[0]
        else:
            minimax = [(self.minimaxDecision(state.generateSuccessor(
                agent, action), depth, agent + 1, init, count + 1)[0], action) for action in actions]
            minimax.sort(key=lambda tup: tup[0])
            return minimax[0]

        # p = currentstate.getAgentPosition(self.index)
        # foods = currentstate.getFood().asList()
        # capsules = currentstate.getCapsules()
        # ghostStates = currentstate.getAgentPosition(self.index)
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
        # score = currentstate.getScore() + 1 / f_dis + 1 / \
        #     h_dis + 1 / c_dis - 1 / g_dis
