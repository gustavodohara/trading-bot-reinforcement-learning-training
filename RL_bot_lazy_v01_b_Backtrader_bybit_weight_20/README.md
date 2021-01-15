# RL_bot_lazy_v05
A bot its use Reinforcement Learning to "learn" actions to buy, sell and hold from course "Financial Engineering and Artificial Intelligence in Python"

This bot use the same model that RL_bot_lazy_v18 but the rewarid is calculates without punishment

The bot is integrated with the backtrade framework

This is a variation of RL_bot_lazy_and_Backtrader_v12_bybit_weight_30 with the addition of a win/loss by month

Train set 80%
Test set 20%

# Status
This bot is in progress

# Installation and Setup Instructions

Clone this repository. You need python 3.6 or higher

## Installation

## To Run

### Training mode
To make this bot learn run:

`python3 step03_q_learning_deterministic.py --fromdate=2019-01-01T04:00:00 --todate=2020-08-06T04:30:00` 
 
### Test mode
To make this bot test run:

`python3 step03_q_learning_deterministic.py --fromdate=2020-08-06T05:00:00 --todate=2020-12-30T12:30:00`

### base line train
`python3 step02_buy_and_hold_once.py --fromdate=2019-01-01T04:00:00 --todate=2020-08-06T04:30:00`

### base line test
`python3 step02_buy_and_hold_once.py --fromdate=2020-08-06T05:00:00 --todate=2020-12-30T12:30:00`



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
Starting Portfolio Value: 100.00
MONTH STATISTICS
DATE 2019-01-02 00:00:00   portfolio 100.00    earn/loss 0.00  (roi 0.00%)
DATE 2019-02-01 00:00:00   portfolio 78.10    earn/loss -21.90  (roi -0.22%)
DATE 2019-03-01 00:00:00   portfolio 74.72    earn/loss -3.39  (roi -0.04%)
DATE 2019-04-01 00:00:00   portfolio 76.83    earn/loss 2.12  (roi 0.03%)
DATE 2019-05-01 00:00:00   portfolio 87.04    earn/loss 10.21  (roi 0.13%)
DATE 2019-06-01 00:00:00   portfolio 110.15    earn/loss 23.11  (roi 0.27%)
DATE 2019-07-01 00:00:00   portfolio 106.46    earn/loss -3.69  (roi -0.03%)
DATE 2019-08-01 00:00:00   portfolio 79.68    earn/loss -26.78  (roi -0.25%)
DATE 2019-09-01 00:00:00   portfolio 86.57    earn/loss 6.89  (roi 0.09%)
DATE 2019-10-01 00:00:00   portfolio 79.10    earn/loss -7.47  (roi -0.09%)
DATE 2019-11-01 00:00:00   portfolio 77.65    earn/loss -1.46  (roi -0.02%)
DATE 2019-12-01 00:00:00   portfolio 72.31    earn/loss -5.34  (roi -0.07%)
DATE 2020-01-01 00:00:00   portfolio 70.40    earn/loss -1.91  (roi -0.03%)
DATE 2020-02-01 00:00:00   portfolio 75.65    earn/loss 5.25  (roi 0.07%)
DATE 2020-03-01 00:00:00   portfolio 71.81    earn/loss -3.84  (roi -0.05%)
DATE 2020-04-01 00:00:00   portfolio 59.24    earn/loss -12.56  (roi -0.17%)
DATE 2020-05-01 00:00:00   portfolio 67.67    earn/loss 8.43  (roi 0.14%)
DATE 2020-06-01 00:00:00   portfolio 66.86    earn/loss -0.81  (roi -0.01%)
DATE 2020-07-01 00:00:00   portfolio 66.07    earn/loss -0.79  (roi -0.01%)
DATE 2020-08-01 00:00:00   portfolio 69.45    earn/loss 3.38  (roi 0.05%)
DATE 2020-08-06   portfolio 67.44    earn/loss -2.02  (roi -0.03%)
total -32.56
MONTH STATISTICS FINISH
2020-08-06, 04:30:00, LAST CLOSE 11655.50
ROI:        -32.56%
finish Portfolio Value: 67.44







#### After Running Test
Starting Portfolio Value: 100.00
MONTH STATISTICS
DATE 2020-08-06 00:00:00   portfolio 100.00    earn/loss 0.00  (roi 0.00%)
DATE 2020-09-01 00:00:00   portfolio 98.23    earn/loss -1.77  (roi -0.02%)
DATE 2020-10-01 00:00:00   portfolio 98.11    earn/loss -0.12  (roi -0.00%)
DATE 2020-11-01 00:00:00   portfolio 95.30    earn/loss -2.81  (roi -0.03%)
DATE 2020-12-01 00:00:00   portfolio 120.84    earn/loss 25.55  (roi 0.27%)
DATE 2020-12-29   portfolio 142.06    earn/loss 21.22  (roi 0.18%)
total 42.06
MONTH STATISTICS FINISH
2020-12-29, 16:30:00, LAST CLOSE 26769.50
ROI:        42.06%  
finish Portfolio Value: 142.06





### Base line
The base line is buy the first day and hold all the stock until the last day without do any operation

#### Base line for train
Starting Portfolio Value: 100.00
2019-01-02, 03:00:00, FIRST CLOSE 3880.00
2020-08-06, 04:30:00, LAST CLOSE 11655.50
ROI:        200.40%
finish Portfolio Value: 300.40
    


#### Base line of Test
Starting Portfolio Value: 100.00
2020-08-06, 05:30:00, FIRST CLOSE 11718.00
2020-12-29, 16:30:00, LAST CLOSE 26769.50
ROI:        128.45%
finish Portfolio Value: 228.45





##Conclusions
the bot works much better than the buy and hold strategy.
I can see by the graph that the bot loss money in big decrease of price (from a high price to a lower price in a small period). Maybe with a stop loss I cad decrease that loss



# References and Additional Reading

* https://www.udemy.com/course/ai-finance/learn/lecture/22084988#overview
* https://sites.google.com/view/machine-learning-ghd/p%C3%A1gina-principal/financial-engeneering-and-artificial-intelligence-in-python/vip-reinforcement-learning-for-algorithmic-trading/trend-following-strategy-with-rl-api
* https://www.backtrader.com/