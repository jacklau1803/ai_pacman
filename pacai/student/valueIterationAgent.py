from pacai.agents.learning.value import ValueEstimationAgent
from pacai.util import counter


class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate=0.9, iters=100, **kwargs):
        super().__init__(index)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = counter.Counter()  # A Counter is a dict with default 0

        states = mdp.getStates()
        for i in range(iters):
            currValue = counter.Counter()
            for state in states:
                action = self.getPolicy(state)
                if action is not None:
                    currValue[state] = self.getQValue(state, action)

            self.values = currValue

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values[state]

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)

    def getQValue(self, state, action):
        result = 0
        tps = self.mdp.getTransitionStatesAndProbs(state, action)
        for nextState, probs in tps:
            result += probs * (self.mdp.getReward(state, action, nextState)
                               + (self.discountRate * self.values[nextState]))
        return result

    def getPolicy(self, state):
        actions = self.mdp.getPossibleActions(state)
        if len(actions) == 0:
            return None
        maxQ = self.getQValue(state, actions[0])
        maxAction = actions[0]
        for action in actions:
            q = self.getQValue(state, action)
            if maxQ < q:
                maxQ = q
                maxAction = action
        return maxAction
