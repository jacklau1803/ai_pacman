"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None


def question2():
    """
    Tested different values in terminal one by one.
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise


def question3a():
    """
    Tested different values in terminal one by one.
    """

    answerDiscount = 0.01
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward


def question3b():
    """
    Tested different values in terminal one by one.
    """

    answerDiscount = 0.2
    answerNoise = 0.2
    answerLivingReward = -0.1

    return answerDiscount, answerNoise, answerLivingReward


def question3c():
    """
    Tested different values in terminal one by one.
    """

    answerDiscount = 0.5
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward


def question3d():
    """
    Tested different values in terminal one by one.
    """

    answerDiscount = 0.9
    answerNoise = 0.5
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward


def question3e():
    """
    Tested different values in terminal one by one.
    """

    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = 10

    return answerDiscount, answerNoise, answerLivingReward


def question6():
    """
    Tested different values in terminal one by one.
    """
    return NOT_POSSIBLE


if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
