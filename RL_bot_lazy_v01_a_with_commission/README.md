# RL_bot_lazy_v20
A bot its use Reinforcement Learning to "learn" actions to buy, sell and hold from course "Financial Engineering and Artificial Intelligence in Python"

This bot use the same logic and training than that RL_bot_lazy_v18 but this time the bot will add a commission

commission of 0.01%, for simplification when BUY or SELL apply the same commission

# Status
This bot is in progress

# Installation and Setup Instructions

Clone this repository. You need python 3.6 or higher

## Installation

## To Run

### Training mode
To make this bot learn run:

`python3 step02_q_learning_trader.py -m train && python3 step03_plot_q_learning_rewards.py -m train` 
 
### Test mode
To make this bot test run:

`python3 step02_q_learning_trader.py -m test && python3 step03_plot_q_learning_rewards.py -m test`

### base line train
`python3 base_line_buy_and_hold.py -m train`

### base line test
`python3 base_line_buy_and_hold.py -m test`

## deterministic

### training mode
 `python3 step05_deterministic_trader.py -m train && python3 step06_plot_trading_and_signals.py -m train`

### test mode
`python3 step05_deterministic_trader.py -m test && python3 step06_plot_trading_and_signals.py -m test`

# Problem to solve
This bot tries to buy/sell 1 asset:
* BTC

# Design

It is a Reinforcement Learning Problem so, we define its component this way:
## State
It use Bins, see https://sites.google.com/view/machine-learning-ghd/p%C3%A1gina-principal/financial-engeneering-and-artificial-intelligence-in-python/vip-reinforcement-learning-for-algorithmic-trading/q-learning-en-el-contexto-de-algorithmic-trading


## Actions
* buy
* sell
* hold: do nothing


2) The agent is a RL use Q-learn 

For simplification also no commission or fee is added


## Rewards
The rewards will be the logReturn: Log of the 'close' price differenced with the close of the previous close


for more info: https://sites.google.com/view/machine-learning-ghd/p%C3%A1gina-principal/financial-engeneering-and-artificial-intelligence-in-python/vip-reinforcement-learning-for-algorithmic-trading/trend-following-strategy-with-rl-api


# Results and Reflections

#### After running Training 
average reward: -164.47, min: -168.35, max: -160.35
average percentage earn/loss: 0.00%, min: 0.00%, max: 0.00%





#### After Running Test
average reward: -39.34, min: -39.67, max: -38.92
average percentage earn/loss: 0.00%, min: 0.00%, max: 0.00%






### Base line
The base line is buy the first day and hold all the stock until the last day without do any operation

#### Base line for train
fist state [4261.45]
last state [10275.96]
env.total_buy_and_hold [6014.51]
reward 0.8801977087213562
percentage earn/loss  2.41%



#### Base line of Test
fist state [10268.11]
last state [10902.]
env.total_buy_and_hold [633.89]
reward 0.059903282796149426
percentage earn/loss  1.06%




##Conclusions
with a punish of -0.1 when the same action is repeat que reward is negative. Also in the graph you can see les repetition of actions but still you can see a lot of the same sequence


# References and Additional Reading

* https://www.udemy.com/course/ai-finance/learn/lecture/22084988#overview
* https://sites.google.com/view/machine-learning-ghd/p%C3%A1gina-principal/financial-engeneering-and-artificial-intelligence-in-python/vip-reinforcement-learning-for-algorithmic-trading/trend-following-strategy-with-rl-api
