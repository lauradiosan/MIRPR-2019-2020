
from dqn.deep_q import DeepQAgent
import os
from datetime import datetime
import numpy as np
import gym
from gym import wrappers
import keras

env = gym.make('LunarLander-v2')
filename = os.path.basename(__file__).split('.')[0]
monitor_dir = './' + str(filename) + '_' + str(datetime.now().date()) + '__' + str(datetime.now().time().second)
env = wrappers.Monitor(env, monitor_dir)

agent = DeepQAgent(env.action_space.n, env.observation_space.shape[0])
done = False
env.reset()
'''
for _ in range(20000):
    observation, reward, done, info = env.step(env.action_space.sample())
    env.render()
    if done:
        env.reset()
'''
state = env.reset()
total = 0
agent.model = keras.models.load_model("good_agent.h5")
while not done:
    state = np.reshape(state, (1, 8))
    action = agent.act(state)
    env.render()
    obs, reward, done, info = env.step(action)
    total += reward
    state = obs
print(f'Episode ended with reward: {total}')

env.close()
