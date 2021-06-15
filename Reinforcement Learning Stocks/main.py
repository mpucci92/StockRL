import gym
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO
from StockEnvironment import *
import pandas as pd

if __name__ == '__main__':

    ticker = 'TSLA'

    df = pd.read_csv(f"Data\\{ticker}.csv")
    df = df.sort_values('Date')

    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([lambda: StockTradingEnv(df)])

    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=2000)

    obs = env.reset()
    for i in range(200):
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        print(env.render())