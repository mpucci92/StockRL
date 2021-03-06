# StockRL
Assignment for Reinforcement Learning - McGill University

Instructions on how to use StockRL Agent

1. `GetData.py`
This script is used to obtain the stock data that the RL agent will use to train on.
The input parameters will be the ticker, the start date and the end date and it will
return a CSV file of the ticker data from the start date till the end date. The CSV will
be saved in the local directory "Data" folder. 


2. `StockEnvironment.py` 
This script you have the option to specify the initial account balance that the agent
will use as a starting grounds. You can also specify the maximum number of shares, the 
maximum share price, the maximum simultaneous open positions, the maximum steps that the RL
Agent will do per training. 

The limits for the reward is defined as well via the reward range: Defining the reward range, 0 to our theoretical max gains from stocks.
The actions sapce is defined as the following actions: Buy x (%), Sell x (%) or Hold (Do nothing).
The observation space is defined as the following: Prices contains the OHLCV values for the last five prices. Note: The amount of days can be changed, but the shape
in the observation space has to reflect accordingly. 

The next_observation class method is used to get the stock data points for the last 5 days and scale them between 0-1 - Normalizing the values
Note the normalization could be done more efficiently, right now it is using the max share price as the denominator to normalize.

The _take_action class method is used to define the actions of buying, selling or holding. 

Step class method is used to execute one time step within the environment.
Reset class method is used to reset the environment - back to the original settings - original cash postion and no shares held yet.
LAstly, the Render class method will Render the environment to the screen.

3. `Main.py`
You need to specify the ticker name you downloaded in the ticker variable.
Proximal Policy Optimization Agent (Model) takes in a Policy, our custom environment and a verbose setting. 
The agent then has a total number of timesteps to learn from.
we reset the environment.
We lastly specify the iterations to execute, and based on an observation, action and states are returned.
Finally, after taking in an action, we can calculate the reward (which we attempt to maximize our cumulative balance over each timestep). 

4. `DQN.py`: This file is used to outline the DQN Class used to create a DQN Object to be used to train a DQN Agent on Open High Low Close stock data
