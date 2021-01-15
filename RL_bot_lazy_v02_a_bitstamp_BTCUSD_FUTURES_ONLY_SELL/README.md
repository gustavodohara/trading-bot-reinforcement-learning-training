# RL_bot_lazy_v20
A bot its use Reinforcement Learning to "learn" actions to buy, sell and hold from course "Financial Engineering and Artificial Intelligence in Python"

future but only sell

exchange: bitstamp

Training set 80%
Test set 20%

# Status
This bot is in done

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
`python3 step04_base_line_buy_and_hold.py -m train`

### base line test
`python3 step04_base_line_buy_and_hold.py -m test`

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
The rewards will be the logReturn: Log of the 'close' price difference with the close of the previous close


for more info: https://sites.google.com/view/machine-learning-ghd/p%C3%A1gina-principal/financial-engeneering-and-artificial-intelligence-in-python/vip-reinforcement-learning-for-algorithmic-trading/trend-following-strategy-with-rl-api


# Results and Reflections

#### After running Training 
average reward: 0.12, min: -1.34, max: 1.53
average percentage earn/loss: 1.12%, min: 0.26%, max: 4.62%



#### After Running Test
average reward: -0.06, min: -0.23, max: 0.20
average percentage earn/loss: 0.94%, min: 0.80%, max: 1.23%






### Base line
The base line is buy the first day and hold all the stock until the last day without do any operation

#### Base line for train
buy and hold quantity test set 21196
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
train_data from BTC    332.56
Name: 2014-12-17 03:00:00+00:00, dtype: float64 to BTC    7965.6
Name: 2019-10-16 16:30:00+00:00, dtype: float64 
test_data from BTC    7954.13
Name: 2019-10-16 17:00:00+00:00, dtype: float64 to BTC    28803.69
Name: 2020-12-30 20:00:00+00:00, dtype: float64 
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
fist state [332.56]
last state [7965.6]
env.total_buy_and_hold [7633.04]
reward 3.1760672541294923


#### Base line of Test
buy and hold quantity test set 21196
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
train_data from BTC    332.56
Name: 2014-12-17 03:00:00+00:00, dtype: float64 to BTC    7965.6
Name: 2019-10-16 16:30:00+00:00, dtype: float64 
test_data from BTC    7954.13
Name: 2019-10-16 17:00:00+00:00, dtype: float64 to BTC    28803.69
Name: 2020-12-30 20:00:00+00:00, dtype: float64 
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
fist state [7954.13]
last state [28803.69]
env.total_buy_and_hold [20849.56]
reward 1.286812213304783
percentage earn/loss  3.62%



##Conclusions



# References and Additional Reading

* https://www.udemy.com/course/ai-finance/learn/lecture/22084988#overview
* https://sites.google.com/view/machine-learning-ghd/p%C3%A1gina-principal/financial-engeneering-and-artificial-intelligence-in-python/vip-reinforcement-learning-for-algorithmic-trading/trend-following-strategy-with-rl-api
