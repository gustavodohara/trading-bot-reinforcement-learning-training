    # RL_bot_lazy_v05
A bot its use Reinforcement Learning to "learn" actions to buy, sell and hold from course "Financial Engineering and Artificial Intelligence in Python"

The bot is integrated with the backtrade framework

exchange bitstamp

symbol ethusd

Train set 80%
Test set 20%

for FUTURES (BUY AND SELL)

bins 30

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
DATE 2015-01-01 00:00:00   portfolio 103.30    earn/loss 3.30  (roi 0.03%)
DATE 2015-02-01 00:00:00   portfolio 273.25    earn/loss 169.94  (roi 1.65%)
DATE 2015-03-01 00:00:00   portfolio 319.11    earn/loss 45.87  (roi 0.17%)
DATE 2015-04-01 00:00:00   portfolio 379.11    earn/loss 59.99  (roi 0.19%)
DATE 2015-05-01 00:00:00   portfolio 424.11    earn/loss 45.00  (roi 0.12%)
DATE 2015-06-01 00:00:00   portfolio 438.94    earn/loss 14.83  (roi 0.03%)
DATE 2015-07-01 00:00:00   portfolio 442.27    earn/loss 3.32  (roi 0.01%)
DATE 2015-08-01 00:00:00   portfolio 387.01    earn/loss -55.25  (roi -0.12%)
DATE 2015-09-01 00:00:00   portfolio 418.01    earn/loss 31.00  (roi 0.08%)
DATE 2015-10-01 00:00:00   portfolio 443.88    earn/loss 25.87  (roi 0.06%)
DATE 2015-11-01 00:00:00   portfolio 431.52    earn/loss -12.35  (roi -0.03%)
DATE 2015-12-01 00:00:00   portfolio 501.68    earn/loss 70.16  (roi 0.16%)
DATE 2016-01-01 00:00:00   portfolio 556.47    earn/loss 54.79  (roi 0.11%)
DATE 2016-02-01 00:00:00   portfolio 633.55    earn/loss 77.08  (roi 0.14%)
DATE 2016-03-01 00:00:00   portfolio 718.36    earn/loss 84.81  (roi 0.13%)
DATE 2016-04-01 00:00:00   portfolio 860.29    earn/loss 141.93  (roi 0.20%)
DATE 2016-05-01 00:00:00   portfolio 904.30    earn/loss 44.01  (roi 0.05%)
DATE 2016-06-01 00:00:00   portfolio 961.51    earn/loss 57.21  (roi 0.06%)
DATE 2016-07-01 00:00:00   portfolio 1104.29    earn/loss 142.78  (roi 0.15%)
DATE 2016-08-01 00:00:00   portfolio 1288.10    earn/loss 183.81  (roi 0.17%)
DATE 2016-09-01 00:00:00   portfolio 1173.24    earn/loss -114.87  (roi -0.09%)
DATE 2016-10-01 00:00:00   portfolio 1229.25    earn/loss 56.01  (roi 0.05%)
DATE 2016-11-01 00:00:00   portfolio 1347.67    earn/loss 118.42  (roi 0.10%)
DATE 2016-12-01 00:00:00   portfolio 1396.33    earn/loss 48.66  (roi 0.04%)
DATE 2017-01-01 00:00:00   portfolio 1366.56    earn/loss -29.77  (roi -0.02%)
DATE 2017-02-01 00:00:00   portfolio 2349.58    earn/loss 983.02  (roi 0.72%)
DATE 2017-03-01 00:00:00   portfolio 2880.70    earn/loss 531.12  (roi 0.23%)
DATE 2017-04-01 00:00:00   portfolio 3102.84    earn/loss 222.14  (roi 0.08%)
DATE 2017-05-01 00:00:00   portfolio 3462.55    earn/loss 359.71  (roi 0.12%)
DATE 2017-06-01 00:00:00   portfolio 4721.21    earn/loss 1258.66  (roi 0.36%)
DATE 2017-07-01 00:00:00   portfolio 7235.02    earn/loss 2513.82  (roi 0.53%)
DATE 2017-08-01 00:00:00   portfolio 9510.33    earn/loss 2275.31  (roi 0.31%)
DATE 2017-09-01 00:00:00   portfolio 11433.31    earn/loss 1922.98  (roi 0.20%)
DATE 2017-10-01 00:00:00   portfolio 15297.59    earn/loss 3864.27  (roi 0.34%)
DATE 2017-11-01 00:00:00   portfolio 21341.52    earn/loss 6043.93  (roi 0.40%)
DATE 2017-12-01 00:00:00   portfolio 37595.01    earn/loss 16253.50  (roi 0.76%)
DATE 2018-01-01 00:00:00   portfolio 59965.08    earn/loss 22370.07  (roi 0.60%)
DATE 2018-02-01 00:00:00   portfolio 268232.62    earn/loss 208267.54  (roi 3.47%)
DATE 2018-03-01 00:00:00   portfolio 850423.11    earn/loss 582190.49  (roi 2.17%)
DATE 2018-04-01 00:00:00   portfolio 1037056.26    earn/loss 186633.14  (roi 0.22%)
DATE 2018-05-01 00:00:00   portfolio 2009948.45    earn/loss 972892.20  (roi 0.94%)
DATE 2018-06-01 00:00:00   portfolio 1989363.92    earn/loss -20584.53  (roi -0.01%)
DATE 2018-07-01 00:00:00   portfolio 2654133.04    earn/loss 664769.12  (roi 0.33%)
DATE 2018-08-01 00:00:00   portfolio 2851922.19    earn/loss 197789.15  (roi 0.07%)
DATE 2018-09-01 00:00:00   portfolio 4638253.61    earn/loss 1786331.42  (roi 0.63%)
DATE 2018-10-01 00:00:00   portfolio 5668213.53    earn/loss 1029959.92  (roi 0.22%)
DATE 2018-11-01 00:00:00   portfolio 6130611.79    earn/loss 462398.26  (roi 0.08%)
DATE 2018-12-01 00:00:00   portfolio 8116989.44    earn/loss 1986377.65  (roi 0.32%)
DATE 2019-01-01 00:00:00   portfolio 11108482.26    earn/loss 2991492.82  (roi 0.37%)
DATE 2019-02-01 00:00:00   portfolio 13737320.19    earn/loss 2628837.93  (roi 0.24%)
DATE 2019-03-01 00:00:00   portfolio 18209710.30    earn/loss 4472390.12  (roi 0.33%)
DATE 2019-04-01 00:00:00   portfolio 20345363.13    earn/loss 2135652.83  (roi 0.12%)
DATE 2019-05-01 00:00:00   portfolio 22886418.64    earn/loss 2541055.51  (roi 0.12%)
DATE 2019-06-01 00:00:00   portfolio 37573392.96    earn/loss 14686974.32  (roi 0.64%)
DATE 2019-07-01 00:00:00   portfolio 69821199.63    earn/loss 32247806.67  (roi 0.86%)
DATE 2019-08-01 00:00:00   portfolio 88200690.05    earn/loss 18379490.42  (roi 0.26%)
DATE 2019-09-01 00:00:00   portfolio 130981505.84    earn/loss 42780815.79  (roi 0.49%)
DATE 2019-10-01 00:00:00   portfolio 191613529.73    earn/loss 60632023.88  (roi 0.46%)
DATE 2019-10-16   portfolio 199551643.68    earn/loss 7938113.96  (roi 0.04%)
total 199551543.68
MONTH STATISTICS FINISH
2019-10-16, 16:30:00, LAST CLOSE 7965.60
ROI:        199551543.68%
Trade Analysis Results:
               Total Open     Total Closed   Total Won      Total Lost     
               1              19593          10500          9093           
               Strike Rate    Win Streak     Losing Streak  PnL Net        
               53.5905680600214413             14             199581113.43   
----------------------------------------
1.6 – 1.9 Below average
2.0 – 2.4 Average
2.5 – 2.9 Good
3.0 – 5.0 Excellent
5.1 – 6.9 Superb
7.0 – Holy Grail?
SQN: 5.12
----------------------------------------
finish Portfolio Value: 199551643.68




#### After Running Test
MONTH STATISTICS
DATE 2019-10-16 00:00:00   portfolio 100.00    earn/loss 0.00  (roi 0.00%)
DATE 2019-11-01 00:00:00   portfolio 94.33    earn/loss -5.67  (roi -0.06%)
DATE 2019-12-01 00:00:00   portfolio 92.04    earn/loss -2.29  (roi -0.02%)
DATE 2020-01-01 00:00:00   portfolio 97.37    earn/loss 5.33  (roi 0.06%)
DATE 2020-02-01 00:00:00   portfolio 111.05    earn/loss 13.68  (roi 0.14%)
DATE 2020-03-01 00:00:00   portfolio 109.02    earn/loss -2.03  (roi -0.02%)
DATE 2020-04-01 00:00:00   portfolio 236.76    earn/loss 127.74  (roi 1.17%)
DATE 2020-05-01 00:00:00   portfolio 232.95    earn/loss -3.80  (roi -0.02%)
DATE 2020-06-01 00:00:00   portfolio 221.71    earn/loss -11.24  (roi -0.05%)
DATE 2020-07-01 00:00:00   portfolio 208.39    earn/loss -13.33  (roi -0.06%)
DATE 2020-08-01 00:00:00   portfolio 192.54    earn/loss -15.84  (roi -0.08%)
DATE 2020-09-01 00:00:00   portfolio 175.69    earn/loss -16.85  (roi -0.09%)
DATE 2020-10-01 00:00:00   portfolio 167.46    earn/loss -8.22  (roi -0.05%)
DATE 2020-11-01 00:00:00   portfolio 166.42    earn/loss -1.04  (roi -0.01%)
DATE 2020-12-01 00:00:00   portfolio 215.55    earn/loss 49.13  (roi 0.30%)
DATE 2020-12-30   portfolio 260.67    earn/loss 45.11  (roi 0.21%)
total 160.67
MONTH STATISTICS FINISH
2020-12-30, 20:00:00, LAST CLOSE 28803.69
ROI:        160.67%
Trade Analysis Results:
               Total Open     Total Closed   Total Won      Total Lost     
               1              4875           2488           2387           
               Strike Rate    Win Streak     Losing Streak  PnL Net        
               51.0358974358974415             12             160.76         
----------------------------------------
1.6 – 1.9 Below average
2.0 – 2.4 Average
2.5 – 2.9 Good
3.0 – 5.0 Excellent
5.1 – 6.9 Superb
7.0 – Holy Grail?
SQN: 1.49
----------------------------------------
finish Portfolio Value: 260.67












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