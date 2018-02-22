from gobang import envs
import random

env = envs.Env()
env.reset()

while True:
    point = random.randint(0, 63)
    state_prime, reward, done, msg = env.step(point)
    if len(msg) != 0:
        print(msg, point)
    else:
        print(reward, done)

    if done:
        break