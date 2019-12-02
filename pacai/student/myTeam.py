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

class AlphaBetaAgent(ReflexCaptureAgent):

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def evaluationFunction(self, state):
        pos = state.getAgentPosition(self.index)
        nf = 1
        ng = 1
        np = 1
        if state.isOnBlueTeam(self.index):
            ghosts = [state.getAgentPosition(g)
                for g in state.getRedTeamIndices() if state.isOnRedSide(state.getAgentPosition(g))]
            pacman = [state.getAgentPosition(p)
                for p in state.getRedTeamIndices() if state.isOnBlueSide(state.getAgentPosition(p))]
            foods = state.getRedFood().asList()
            capsules = state.getRedCapsules()
            f_dis = [self.getMazeDistance(pos, food) for food in foods]
            g_dis = [self.getMazeDistance(pos, ghost) for ghost in ghosts]
            p_dis = [self.getMazeDistance(pos, pac) for pac in pacman]
            if f_dis:
                nf = min(f_dis)
            if g_dis:
                ng = min(g_dis)
            if p_dis:
                np = min(p_dis)
            if state.isOnRedSide(pos):
                score = 1 / nf - 1 / ng - len(foods)
            elif p_dis:
                score = 1 / np - len(p_dis)
            else:
                score = 1 / nf - len(foods)
            # g_dis = 0
            # f_dis = 0
            # for ghost in ghosts:
            #     g_dis += self.getMazeDistance(pos, ghost)
            # for food in foods:
            #     f_dis += self.getMazeDistance(pos, food)
        else:
            ghosts = [state.getAgentPosition(g)
                for g in state.getBlueTeamIndices() if state.isOnBlueSide(state.getAgentPosition(g))]
            pacman = [state.getAgentPosition(p)
                for p in state.getRedTeamIndices() if state.isOnBlueSide(state.getAgentPosition(p))]
            foods = state.getBlueFood().asList()
            capsules = state.getBlueCapsules()
            f_dis = [self.getMazeDistance(pos, food) for food in foods]
            g_dis = [self.getMazeDistance(pos, ghost) for ghost in ghosts]
            p_dis = [self.getMazeDistance(pos, pac) for pac in pacman]
            if f_dis:
                nf = min(f_dis)
            if g_dis:
                ng = min(g_dis)
            if p_dis:
                np = min(p_dis)
            if state.isOnBlueSide(pos):
                score = 1 / nf - 1 / ng - len(foods)
            elif p_dis:
                score = 1 / np - len(p_dis)
            else:
                score = 1 / nf - len(foods)
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
            if abs(init - agent - 1) != 2:
                minimax = [(self.minimaxDecision(state.generateSuccessor(
                    agent, action), depth, agent + 1, init, count + 1)[0], action) for action in actions]
            else:
                minimax = [(self.minimaxDecision(state.generateSuccessor(
                    agent, action), depth, agent + 2, init, count + 1)[0], action) for action in actions]
            minimax.sort(key=lambda tup: tup[0])
            return minimax[0]
