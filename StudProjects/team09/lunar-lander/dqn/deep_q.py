from collections import deque
import keras
import numpy as np
import random
import gym
import matplotlib.pyplot as plt
import logging
from gym import wrappers
import os
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DeepQAgent:
    def __init__(self,
                 nr_actions,
                 nr_states,
                 epsilon_init=1.0,
                 epsilon_min=0.1,
                 alpha=0.001,
                 gamma=.99,
                 batch_size=64,
                 epsilon_decay=.996,  # to decrease epsilon by *
                 max_replay_memory_size=10 ** 7):
        self.actions = nr_actions
        self.states = nr_states
        self.epsilon = epsilon_init
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.gamma = gamma
        self.alpha = alpha
        self.batch_size = batch_size
        self.replay_memory = deque(maxlen=max_replay_memory_size)
        self.model = self.build_model()

    def build_model(self):
        model = keras.Sequential()  # layer by layer
        model.add(keras.layers.Dense(150, input_dim=self.states, activation=keras.activations.relu))
        model.add(keras.layers.Dense(120, activation=keras.activations.relu))
        model.add(keras.layers.Dense(self.actions, activation=keras.activations.linear))
        # compile network model with mean squared error as loss function and with adam optimizer
        model.compile(loss='mse', optimizer=keras.optimizers.adam(lr=self.alpha))
        return model

    def memorize(self, state, action, reward, next_state, done):
        self.replay_memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.replay_memory) < self.batch_size:
            return
        batch = random.sample(population=self.replay_memory, k=self.batch_size)
        states, actions, rewards, next_states, dones = list(zip(*batch))

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        actions = np.array(actions)
        rewards = np.array(rewards)
        dones = np.array(dones)

        targets = rewards + self.gamma * (np.amax(self.model.predict_on_batch(next_states), axis=1)) * (1 - dones)
        targets_full = self.model.predict_on_batch(states)
        indices = np.array(range(self.batch_size))
        targets_full[[indices], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        self.epsilon *= self.epsilon_decay if self.epsilon > self.epsilon_min else 1

    def act(self, state):
        logging.info(f'{state} i do')
        # logger.info(f'{state} i do')

        if random.random() <= self.epsilon:
            return random.randrange(self.actions)
        action_values = self.model.predict(state)
        return np.argmax(action_values[0])  # index of max value


def demo(env, agent):
    filename = os.path.basename(__file__).split('.')[0]
    this_moment = datetime.now()
    monitor_dir = './' + str(filename) + '_' + str(this_moment.date()) + '__' + str(this_moment.time().minute) + '__' + str(this_moment.time().second)
    env = wrappers.Monitor(env, monitor_dir)
    state = env.reset()
    total = 0
    done = False
    while not done:
        state = np.reshape(state, (1, 8))
        action = agent.act(state)
        env.render()
        obs, reward, done, info = env.step(action)
        total += reward
        state = obs
    logger.info(f'Episode ended with reward: {total}')
    print(f'Episode ended with reward: {total}')


def train_agent(env, nr_episodes=1000, render=False, reward_threshold=200, running_avg_len=100):
    loss = []
    # will store average of last running_avg_len episodes
    running_avgs = []
    agent = DeepQAgent(env.action_space.n, env.observation_space.shape[0])
    for episode in range(nr_episodes):
        logger.info("Running episode {}".format(episode))
        state = np.reshape(env.reset(), (1, 8))
        score = 0
        max_steps = 3000
        for i in range(max_steps):
            action = agent.act(state)
            if render:
                env.render()
            next_state, reward, done, _ = env.step(action)
            score += reward
            next_state = np.reshape(next_state, (1, 8))
            agent.memorize(state, action, reward, next_state, done)
            state = next_state
            # this is the moment to take one hard look at the replay method again
            agent.replay()
            if done:
                # print('episode done')
                logger.info("Episode: {}/{}, score: {:.2f}".format(episode, nr_episodes, score))
                break
        loss.append(score)

        running_avg = np.mean(loss[-running_avg_len:])
        running_avgs.append(running_avg)
        stop = running_avg > reward_threshold
        if stop:
            logger.info('\n Landing Successful! \n')
            break
        logger.info("Average of last {0} episodes: {1:.2f} \n".format(running_avg_len, running_avg))
    return agent, loss, running_avgs


if __name__ == '__main__':
    gym.envs.register(
        id='LunarLanderCustom-v0',
        entry_point='dqn.harder_env:LunarLanderCustom',
        max_episode_steps=1000,
    )
    env = gym.make('LunarLander-v2')
    trained_agent, losses, running_averages = train_agent(env, reward_threshold=200)
    # plt.plot([i + 1 for i in range(0, len(losses), 2)], losses[::2])
    plt.plot(range(len(running_averages)), running_averages)
    trained_agent.model.save("good_agent.h5")
    # demo(env,trained_agent)
    # demo(env, trained_agent)
    plt.show()
    env.close()
