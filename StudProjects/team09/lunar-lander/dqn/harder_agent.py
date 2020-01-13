import gym

gym.envs.register(
    id='LunarLanderCustom-v0',
    entry_point='dqn.harder_env:LunarLanderCustom',
    max_episode_steps=1000,
)

env = gym.make('LunarLanderCustom-v0')
env.reset()
for _ in range(1000):
    _, _, done, _ = env.step(env.action_space.sample())
    env.render()
    if done:
        env.reset()
env.close()
