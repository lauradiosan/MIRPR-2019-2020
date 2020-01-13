
import gym

if __name__ == '__main__':
    env = gym.make('LunarLander-v2')
    env.reset()
    for _ in range(1000):
        env.render()
        _, _, done, _ = env.step(env.action_space.sample())
        if done:
            env.reset()
    env.close()
