import numpy as np


class Env:
    """
    env, actually the people the actor will face
    """

    def __init__(self, width: int=8, height: int=8):
        self._width = width
        self._height = height
        self._range = self._height * self._width
        self._state = np.zeros([self._range])
        self._action_space = np.arange(self._range)

    def reset(self):
        self._state = np.zeros([self._range])

    def step(self, action:int):
        assert action in self._action_space
        if self._state[action] != 0:
            self._print_state()
            return None, None, False, {'you can not set in this position'}

        self._state[action] = -1
        p1, p2 = self._detect_done()
        if p1 and p2 is None:
            return self._state, 10, True, {}
        else:
            while True:
                point = input('do your action:')
                h, w = map(int, point.split(','))
                if any([h not in np.arange(self._height), w not in np.arange(self._width)]):
                    print('input point not legal')
                else:
                    point = h * self._height + w
                    self._state[point] = 1
                    p1, p2 = self._detect_done()
                    if p1 and p2 is None:
                        return self._state, -10, True, {}
                    else:
                        return self._state, p2 - 5, False, {}

    def _detect_done(self):
        self._print_state()
        point = self._state.reshape([self._height, self._width])
        max_machine = 0
        max_human = 0
        for i in range(self._height):
            for j in range(self._width):
                p = point[i][j]
                if p != 0:
                    print(i, j, p)
                    # for horizontally
                    left = 0
                    right = 0
                    for k in range(j - 1, -1):
                        if point[i][k] == p:
                            left += 1
                        else:
                            break
                    for k in range(j + 1, self._width):
                        if point[i][k] == p:
                            right += 1
                        else:
                            break
                    if left + right >= 4:
                        print(left, right, 1)
                        return True, None

                    # for vertically
                    above = 0
                    below = 0
                    for k in range(i - 1, -1):
                        if point[k][j] == p:
                            above += 1
                        else:
                            break
                    for k in range(i + 1, self._height):
                        if point[k][j] == p:
                            below += 1
                        else:
                            break
                    if above + below >= 4:
                        print(above, below, 2)
                        return True, None

                    if p == 1:
                        max_human = max(max_human, left + right, above + below)
                    else:
                        max_machine = max(max_machine, left + right, above + below)

        return max_human, max_machine


    def _print_state(self):
        print(self._state.reshape([self._height, self._width]))



