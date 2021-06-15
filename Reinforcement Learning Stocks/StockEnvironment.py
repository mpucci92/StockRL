import random
import gym
from gym import spaces
import pandas as pd
import numpy as np

maxAccountBalance = 2000000000
maxNumberShares = 2000000000
maxSharePrice = 10000
maxOpenPositions = 10
maxRLSteps = 10000
accountBalance = 100000

class StockTradingEnv(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, df):

        super(StockTradingEnv, self).__init__()  # "Super" - Used to give access to methods and properties of a parent

        self.df = df  # Stock Environment expects a dataframe as input
        self.reward_range = (
        0, maxAccountBalance)  # Defining the reward range, 0 to our theoretical max gains from stocks

        # Actions which could be too: Buy x (%), Sell x (%) or Hold (Do nothing)
        self.action_space = spaces.Box(
            low=np.array([0, 0]), high=np.array([3, 1]),
            dtype=np.float16)  # Declaring the action_space and observation_space  - Customized declarations

        # Prices contains the OHLC values for the last five prices
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(5, 6), dtype=np.float16)

    def next_observation(self):
        # Get the stock data points for the last 5 days and scale to between 0-1   - Normalizing the values
        # Change the value of 5 if you would like to change the lookbackPeriod for stock data

        dataframe = np.array([
            self.df.loc[self.current_step: self.current_step +
                                           5, 'Open'].values / maxSharePrice,
            self.df.loc[self.current_step: self.current_step +
                                           5, 'High'].values / maxSharePrice,
            self.df.loc[self.current_step: self.current_step +
                                           5, 'Low'].values / maxSharePrice,
            self.df.loc[self.current_step: self.current_step +
                                           5, 'Close'].values / maxSharePrice,
            self.df.loc[self.current_step: self.current_step +
                                           5, 'Volume'].values / maxNumberShares,
        ])

        return dataframe

    def _take_action(self, action):
        # Set the current price to a random price within the time step
        current_price = random.uniform(
            self.df.loc[self.current_step, "Open"], self.df.loc[self.current_step, "Close"])
        action_type = action[0]
        amount = action[1]

        if action_type < 1:
            # Buy amount % of balance in shares
            total_possible = int(self.balance / current_price)
            shares_bought = int(total_possible * amount)
            prev_cost = self.cost_basis * self.shares_held
            additional_cost = shares_bought * current_price

            self.balance = self.balance - additional_cost
            self.cost_basis = (
                                      prev_cost + additional_cost) / (self.shares_held + shares_bought)
            self.shares_held = self.shares_held + shares_bought

        elif action_type < 2:
            # Sell amount % of shares held
            shares_sold = int(self.shares_held * amount)
            self.balance += shares_sold * current_price
            self.shares_held -= shares_sold
            self.total_shares_sold += shares_sold
            self.total_sales_value += shares_sold * current_price

        self.net_worth = self.balance + self.shares_held * current_price

        if self.net_worth > self.max_net_worth:
            self.max_net_worth = self.net_worth

        if self.shares_held == 0:
            self.cost_basis = 0

    def step(self, action):
        # Execute one time step within the environment
        self._take_action(action)

        self.current_step += 1  # add 1 to the current step

        if self.current_step > len(self.df.loc[:, 'Open'].values) - 6:
            self.current_step = 0  # Done the timeseries, reset the current step to 0 in this case.

        # timeBenefit = (self.current_step / maxRLSteps)   # Give

        reward = self.balance  # *  timeBenefit
        done = self.net_worth <= 0

        obs = self.next_observation()

        return obs, reward, done, {}

    def reset(self):
        # Reset the environment - back to the original settings - original cash postion and no shares held yet #
        self.balance = accountBalance
        self.net_worth = accountBalance
        self.max_net_worth = accountBalance
        self.shares_held = 0
        self.cost_basis = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0

        # Set the current step to a random point within the data frame
        self.current_step = random.randint(
            0, len(self.df.loc[:, 'Open'].values) - 6)

        return self.next_observation()

    def render(self, mode='human', close=False):
        # Render the environment to the screen #
        profit = self.net_worth - accountBalance
        print(f'Step: {self.current_step}')
        print(f'Profit: {profit}')
