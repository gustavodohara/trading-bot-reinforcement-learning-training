# RL_bot_lazy_v05
A bot its use Reinforcement Learning to "learn" actions to buy, sell and hold from course "Financial Engineering and Artificial Intelligence in Python"

The bot is integrated with the backtrade framework

exchange bitstamp

symbol ethusd

Train set 80%
Test set 20%

for FUTURES

# Status
This bot is in progress

# Installation and Setup Instructions

Clone this repository. You need python 3.6 or higher

## Installation

## To Run

### Training mode
To make this bot learn run:

`python3 step03_q_learning_deterministic.py --fromdate=2014-12-15T03:00:00 --todate=2019-10-16T16:30:00` 
 
### Test mode
To make this bot test run:

`python3 step03_q_learning_deterministic.py --fromdate=2019-10-16T17:00:00 --todate=2020-12-30T20:30:00`

### base line train
`python3 step02_buy_and_hold_once.py --fromdate=2014-12-15T03:00:00 --todate=2019-10-16T16:30:00`

### base line test
`python3 step02_buy_and_hold_once.py --fromdate=2019-10-16T17:00:00 --todate=2020-12-30T20:30:00`



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
MONTH STATISTICS
DATE 2014-12-17 00:00:00   portfolio 100.00    earn/loss 0.00  (roi 0.00%)
DATE 2015-01-01 00:00:00   portfolio 103.00    earn/loss 3.00  (roi 0.03%)
DATE 2015-02-01 00:00:00   portfolio 89.36    earn/loss -13.64  (roi -0.13%)
DATE 2015-03-01 00:00:00   portfolio 84.19    earn/loss -5.17  (roi -0.06%)
DATE 2015-04-01 00:00:00   portfolio 83.05    earn/loss -1.14  (roi -0.01%)
DATE 2015-05-01 00:00:00   portfolio 80.90    earn/loss -2.16  (roi -0.03%)
DATE 2015-06-01 00:00:00   portfolio 89.57    earn/loss 8.68  (roi 0.11%)
DATE 2015-07-01 00:00:00   portfolio 96.16    earn/loss 6.58  (roi 0.07%)
DATE 2015-08-01 00:00:00   portfolio 95.25    earn/loss -0.91  (roi -0.01%)
DATE 2015-09-01 00:00:00   portfolio 99.45    earn/loss 4.20  (roi 0.04%)
DATE 2015-10-01 00:00:00   portfolio 104.20    earn/loss 4.74  (roi 0.05%)
DATE 2015-11-01 00:00:00   portfolio 100.38    earn/loss -3.82  (roi -0.04%)
DATE 2015-12-01 00:00:00   portfolio 95.69    earn/loss -4.69  (roi -0.05%)
DATE 2016-01-01 00:00:00   portfolio 95.33    earn/loss -0.36  (roi -0.00%)
DATE 2016-02-01 00:00:00   portfolio 96.45    earn/loss 1.11  (roi 0.01%)
DATE 2016-03-01 00:00:00   portfolio 98.43    earn/loss 1.99  (roi 0.02%)
DATE 2016-04-01 00:00:00   portfolio 103.49    earn/loss 5.06  (roi 0.05%)
DATE 2016-05-01 00:00:00   portfolio 103.60    earn/loss 0.12  (roi 0.00%)
DATE 2016-06-01 00:00:00   portfolio 92.48    earn/loss -11.12  (roi -0.11%)
DATE 2016-07-01 00:00:00   portfolio 88.17    earn/loss -4.32  (roi -0.05%)
DATE 2016-08-01 00:00:00   portfolio 82.63    earn/loss -5.54  (roi -0.06%)
DATE 2016-09-01 00:00:00   portfolio 79.14    earn/loss -3.49  (roi -0.04%)
DATE 2016-10-01 00:00:00   portfolio 80.90    earn/loss 1.76  (roi 0.02%)
DATE 2016-11-01 00:00:00   portfolio 81.20    earn/loss 0.30  (roi 0.00%)
DATE 2016-12-01 00:00:00   portfolio 81.88    earn/loss 0.69  (roi 0.01%)
DATE 2017-01-01 00:00:00   portfolio 85.32    earn/loss 3.44  (roi 0.04%)
DATE 2017-02-01 00:00:00   portfolio 88.49    earn/loss 3.17  (roi 0.04%)
DATE 2017-03-01 00:00:00   portfolio 90.44    earn/loss 1.95  (roi 0.02%)
DATE 2017-04-01 00:00:00   portfolio 95.87    earn/loss 5.43  (roi 0.06%)
DATE 2017-05-01 00:00:00   portfolio 92.07    earn/loss -3.81  (roi -0.04%)
DATE 2017-06-01 00:00:00   portfolio 95.64    earn/loss 3.58  (roi 0.04%)
DATE 2017-07-01 00:00:00   portfolio 105.30    earn/loss 9.66  (roi 0.10%)
DATE 2017-08-01 00:00:00   portfolio 113.02    earn/loss 7.71  (roi 0.07%)
DATE 2017-09-01 00:00:00   portfolio 105.74    earn/loss -7.27  (roi -0.06%)
DATE 2017-10-01 00:00:00   portfolio 95.77    earn/loss -9.97  (roi -0.09%)
DATE 2017-11-01 00:00:00   portfolio 92.51    earn/loss -3.26  (roi -0.03%)
DATE 2017-12-01 00:00:00   portfolio 88.34    earn/loss -4.17  (roi -0.05%)
DATE 2018-01-01 00:00:00   portfolio 97.25    earn/loss 8.90  (roi 0.10%)
DATE 2018-02-01 00:00:00   portfolio 103.27    earn/loss 6.02  (roi 0.06%)
DATE 2018-03-01 00:00:00   portfolio 115.12    earn/loss 11.86  (roi 0.11%)
DATE 2018-04-01 00:00:00   portfolio 127.97    earn/loss 12.84  (roi 0.11%)
DATE 2018-05-01 00:00:00   portfolio 129.82    earn/loss 1.85  (roi 0.01%)
DATE 2018-06-01 00:00:00   portfolio 130.83    earn/loss 1.01  (roi 0.01%)
DATE 2018-07-01 00:00:00   portfolio 132.66    earn/loss 1.83  (roi 0.01%)
DATE 2018-08-01 00:00:00   portfolio 129.84    earn/loss -2.82  (roi -0.02%)
DATE 2018-09-01 00:00:00   portfolio 117.85    earn/loss -11.99  (roi -0.09%)
DATE 2018-10-01 00:00:00   portfolio 115.30    earn/loss -2.55  (roi -0.02%)
DATE 2018-11-01 00:00:00   portfolio 124.78    earn/loss 9.48  (roi 0.08%)
DATE 2018-12-01 00:00:00   portfolio 126.26    earn/loss 1.49  (roi 0.01%)
DATE 2019-01-01 00:00:00   portfolio 142.87    earn/loss 16.60  (roi 0.13%)
DATE 2019-02-01 00:00:00   portfolio 142.73    earn/loss -0.13  (roi -0.00%)
DATE 2019-03-01 00:00:00   portfolio 136.10    earn/loss -6.63  (roi -0.05%)
DATE 2019-04-01 00:00:00   portfolio 133.05    earn/loss -3.05  (roi -0.02%)
DATE 2019-05-01 00:00:00   portfolio 130.97    earn/loss -2.08  (roi -0.02%)
DATE 2019-06-01 00:00:00   portfolio 123.69    earn/loss -7.28  (roi -0.06%)
DATE 2019-07-01 00:00:00   portfolio 110.93    earn/loss -12.76  (roi -0.10%)
DATE 2019-08-01 00:00:00   portfolio 124.63    earn/loss 13.69  (roi 0.12%)
DATE 2019-09-01 00:00:00   portfolio 133.64    earn/loss 9.02  (roi 0.07%)
DATE 2019-10-01 00:00:00   portfolio 134.36    earn/loss 0.71  (roi 0.01%)
DATE 2019-10-16   portfolio 139.29    earn/loss 4.94  (roi 0.04%)
total 39.29
MONTH STATISTICS FINISH
2019-10-16, 16:30:00, LAST CLOSE 7965.60
ROI:        39.29%
Trade Analysis Results:
               Total Open     Total Closed   Total Won      Total Lost     
               0              9384           4814           4570           
               Strike Rate    Win Streak     Losing Streak  PnL Net        
               51.300085251491913             10             39.29          
----------------------------------------
1.6 – 1.9 Below average
2.0 – 2.4 Average
2.5 – 2.9 Good
3.0 – 5.0 Excellent
5.1 – 6.9 Superb
7.0 – Holy Grail?
SQN: 0.86
----------------------------------------
finish Portfolio Value: 139.29





#### After Running Test
MONTH STATISTICS
DATE 2019-10-16 00:00:00   portfolio 100.00    earn/loss 0.00  (roi 0.00%)
DATE 2019-11-01 00:00:00   portfolio 100.29    earn/loss 0.29  (roi 0.00%)
DATE 2019-12-01 00:00:00   portfolio 107.42    earn/loss 7.12  (roi 0.07%)
DATE 2020-01-01 00:00:00   portfolio 104.71    earn/loss -2.71  (roi -0.03%)
DATE 2020-02-01 00:00:00   portfolio 102.60    earn/loss -2.10  (roi -0.02%)
DATE 2020-03-01 00:00:00   portfolio 96.84    earn/loss -5.76  (roi -0.06%)
DATE 2020-04-01 00:00:00   portfolio 100.32    earn/loss 3.48  (roi 0.04%)
DATE 2020-05-01 00:00:00   portfolio 95.26    earn/loss -5.07  (roi -0.05%)
DATE 2020-06-01 00:00:00   portfolio 84.51    earn/loss -10.74  (roi -0.11%)
DATE 2020-07-01 00:00:00   portfolio 83.07    earn/loss -1.44  (roi -0.02%)
DATE 2020-08-01 00:00:00   portfolio 81.65    earn/loss -1.42  (roi -0.02%)
DATE 2020-09-01 00:00:00   portfolio 89.77    earn/loss 8.12  (roi 0.10%)
DATE 2020-10-01 00:00:00   portfolio 90.11    earn/loss 0.34  (roi 0.00%)
DATE 2020-11-01 00:00:00   portfolio 83.85    earn/loss -6.26  (roi -0.07%)
DATE 2020-12-01 00:00:00   portfolio 88.32    earn/loss 4.47  (roi 0.05%)
DATE 2020-12-30   portfolio 91.27    earn/loss 2.95  (roi 0.03%)
total -8.73
MONTH STATISTICS FINISH
2020-12-30, 20:00:00, LAST CLOSE 28803.69
ROI:        -8.73%
Trade Analysis Results:
               Total Open     Total Closed   Total Won      Total Lost     
               1              2187           1090           1097           
               Strike Rate    Win Streak     Losing Streak  PnL Net        
               49.8399634202103313             9              -8.77          
----------------------------------------
1.6 – 1.9 Below average
2.0 – 2.4 Average
2.5 – 2.9 Good
3.0 – 5.0 Excellent
5.1 – 6.9 Superb
7.0 – Holy Grail?
SQN: -0.53
----------------------------------------
finish Portfolio Value: 91.27






### Base line
The base line is buy the first day and hold all the stock until the last day without do any operation

#### Base line for train
Starting Portfolio Value: 100.00
2014-12-17, 03:30:00, FIRST CLOSE 332.56
2019-10-16, 16:30:00, LAST CLOSE 7965.60
ROI:        2289.91%
finish Portfolio Value: 2389.91


#### Base line of Test
Starting Portfolio Value: 100.00
2019-10-16, 17:30:00, FIRST CLOSE 7954.13
2020-12-30, 20:00:00, LAST CLOSE 28803.69
ROI:        208.50%
finish Portfolio Value: 308.50







##Conclusions
I do not sure why, but this but give me loos respect to the base line. :()



# References and Additional Reading

* https://www.udemy.com/course/ai-finance/learn/lecture/22084988#overview
* https://sites.google.com/view/machine-learning-ghd/p%C3%A1gina-principal/financial-engeneering-and-artificial-intelligence-in-python/vip-reinforcement-learning-for-algorithmic-trading/trend-following-strategy-with-rl-api
* https://www.backtrader.com/