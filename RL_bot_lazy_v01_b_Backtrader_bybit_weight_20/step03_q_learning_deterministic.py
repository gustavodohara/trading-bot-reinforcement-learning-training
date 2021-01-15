import datetime
import argparse
import backtrader as bt
import pickle
import pandas as pd
import numpy as np
import itertools
import math

INPUT_FILE = '../data/bybit_btc_usd_jan19-dic20_backtrader_30m.csv'

ACTION_SPACE_BUY = 0
ACTION_SPACE_SELL = 1
ACTION_SPACE_HOLD = 2


# REINFORCEMENT LEARNING

# aca definimos los "bins" para convertur algo continuo e infinito (log_returns) en algo discreto y finito
# la idea de esto es convertir un vector continuo de estados al bin correcto
class StateMapper:
    # vamos a recorrer por el environment de forma random para recolectar samples (unas 10.000 veces)
    def __init__(self, d):
        self.D = d  # number of elements we need to bin

        # create the bins for each dimension
        self.bins = []

    def transform(self, state):
        x = np.zeros(self.D)
        for d in range(self.D):
            x[d] = int(np.digitize(state[d], self.bins[d]))
        return tuple(x)

    def all_possible_states(self):
        list_of_bins = []
        for d in range(self.D):
            list_of_bins.append(list(range(len(self.bins[d]) + 1)))
        # print(list_of_bins)
        return itertools.product(*list_of_bins)

    def load(self, filepath):
        # npz = np.load(filepath)

        a_file = open(filepath, "rb")
        bins = pickle.load(a_file)
        print(f"load bins {bins}")
        self.bins = bins


class Agent:
    def __init__(self, action_size, state_mapper):
        self.action_size = action_size
        self.gamma = 0.8  # discount rate
        self.epsilon = 0.1
        self.learning_rate = 1e-1
        self.state_mapper = state_mapper

        # initialize Q-table randomly
        self.Q = {}
        for s in self.state_mapper.all_possible_states():
            s = tuple(s)
            for a in range(self.action_size):
                self.Q[(s, a)] = np.random.randn()

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)

        s = self.state_mapper.transform(state)
        act_values = [self.Q[(s, a)] for a in range(self.action_size)]
        return np.argmax(act_values)  # returns action

    def train(self, state, action, reward, next_state, done):
        s = self.state_mapper.transform(state)
        s2 = self.state_mapper.transform(next_state)

        if done:
            target = reward
        else:
            act_values = [self.Q[(s2, a)] for a in range(self.action_size)]
            target = reward + self.gamma * np.amax(act_values)

        # Run one training step
        self.Q[(s, action)] += self.learning_rate * (target - self.Q[(s, action)])

    def load(self, filepath):
        # npz = np.load(filepath)
        # print(f"load Q of type ${type(npz)}")
        # self.Q = npz
        a_file = open(filepath, "rb")
        q = pickle.load(a_file)
        print(f"load Q ${q}")
        self.Q = q

    def save(self, filepath):
        print(f"saving Q of type ${type(self.Q)}")
        print(f"saving Q ${self.Q}")
        # np.savez_compressed(filepath, self.Q)
        a_file = open(filepath, "wb")
        pickle.dump(self.Q, a_file)
        a_file.close()


# Create a subclass of Strategy to define the indicators and logic

# DATA FEED

class BitcoinFeed(bt.feeds.GenericCSVData):
    params = (
        ('openinterest', -1),
        ('dtformat', '%Y-%m-%d %H:%M:%S'),
        ('tmformat', '%H:%M:%SZ'),
        ('timeframe', bt.TimeFrame.Minutes),  # the data is in minutes
        ('compression', 30),  # mean each bar is 30 minutes
    )


class EndOfMonth(object):

    def __init__(self, cal):
        self.cal = cal

    def __call__(self, d):
        if self.cal.last_monthday(d):
            return True
        return False

# STRATEGY

class Strategy(bt.Strategy):
    params = dict(
        agent=None,
        when=bt.timer.SESSION_START,
        timer=True,
        monthdays=[1],
    )

    def __init__(self):
        self.agent = self.params.agent
        self.BTC = self.datas[0]
        self.dataclose = self.datas[0].close
        # Sentinel to None: new ordersa allowed
        self.orefs = list()
        self.val_start = 0
        self.val_start_month = 0
        self.month_stats = []

        self.add_timer(
            when=self.p.when,
            monthdays=self.p.monthdays,
        )

    def log(self, txt, dt=None):
        ''' Loggin function for this strategy'''
        datetime = self.datas[0].datetime
        date = datetime.date(0).isoformat()
        time = datetime.time()
        print('%s, %s, %s' % (date, time, txt))

    def start(self):
        self.val_start = self.val_start_month = self.broker.get_cash()  # keep the starting cash

        # Add a timer which will be called on the 1st trading day of the month
        # self.add_timer(
        #     bt.timer.SESSION_END,  # when it will be called
        #     monthdays=[1],  # called on the 1st day of the month
        #     monthcarry=True,  # called on the 2nd day if the 1st is holiday
        # )

    def add_month_stats(self, when=None):
        month_val = self.broker.get_value() - self.val_start_month
        roi = (self.broker.get_value() / self.val_start_month) - 1.0
        # month_val = self.broker.get_cash() + self.broker.get_value() - self.val_start_month
        if when:
            date = when
        else:
            month_datetime = self.datas[0].datetime
            date = month_datetime.date(0).isoformat()
        self.val_start_month = self.broker.get_value()
        self.month_stats.append(dict(date=date, portfolio=self.broker.get_value(), value=month_val, roi=roi))

    def notify_timer(self, timer, when, *args, **kwargs):
        self.add_month_stats(when=when)

    def notify_order(self, order):
        if order.status != order.Completed:
            # print('{}: Order ref: {} / Type {} / Status {} / Price {}'.format(
            #     self.data.datetime.date(0),
            #     order.ref, 'Buy' * order.isbuy() or 'Sell',
            #     order.getstatusname(),
            #     order.price)
            # )
            pass
        else:
            # print('{}: Order ref: {} / Type {} / Price {} / Value {} / COMPLETED '.format(
            #     self.data.datetime.date(0),
            #     order.ref, 'Buy' * order.isbuy() or 'Sell',
            #     order.executed.price,
            #     order.executed.value
            # ))
            pass

        if not order.alive() and order.ref in self.orefs:
            self.orefs.remove(order.ref)

    def get_log_return(self):
        log_return = round(math.log(self.dataclose[0]) - math.log(self.dataclose[-1]), 6)
        # print(log_return)
        return [log_return]

    def buy_all(self, asset):
        if self.getposition(asset).size == 0.0:
            size = self.broker.get_cash() / self.data
            o = self.buy(size=size)
            self.orefs.append(o.ref)

    def sell_all(self, asset):
        if self.getposition(asset).size != 0.0:
            o = self.sell()
            self.orefs.append(o.ref)

    def next(self):
        if len(self) <= 1:
            return

        if self.orefs:
            return  # pending orders do nothing

        # the state is the log_return
        state = self.get_log_return()
        action = self.agent.act(state)
        if action == ACTION_SPACE_BUY:
            # self.log('BOT SAID BUY!!!')
            self.buy_all(self.BTC)
        elif action == ACTION_SPACE_SELL:
            # self.log('BOT SAID SELL!!!!!!!')
            self.sell_all(self.BTC)

    def stop(self):
        # calculate last month stats
        self.add_month_stats()
        # print month stats
        self.print_stats_month()
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        self.log('LAST CLOSE %.2f' % (self.datas[0].close[0]))
        print('ROI:        {:.2f}%'.format(100.0 * self.roi))

    def print_stats_month(self):
        print('MONTH STATISTICS')
        total = 0
        for i in self.month_stats:
            print('DATE {}   portfolio {:.2f}    earn/loss {:.2f}  (roi {:.2f}%)'.format(i['date'], i['portfolio'], i['value'], i['roi']))
            total += i['value']

        print('total {:.2f}'.format(total))
        print('MONTH STATISTICS FINISH')


# RUN
def run(args=None):
    args = parse_args(args)

    # config
    models_folder = 'q_learning_rl_trader_models'

    D = 1
    action_space = [ACTION_SPACE_BUY, ACTION_SPACE_SELL, ACTION_SPACE_HOLD]  # BUY, SELL, HOLD

    state_mapper = StateMapper(D)

    # then load previous state_mapper
    state_mapper.load(f'{models_folder}/state_mapper.pkl')

    action_size = len(action_space)
    agent = Agent(action_size, state_mapper)

    # If epsilon is 0 then is deterministics (the rewards are alwais the same!)
    agent.epsilon = 0.00

    # load trained weights
    agent.load(f'{models_folder}/q.pkl')

    print(state_mapper.bins)

    # Data feed kwargs
    kwargs = dict(dataname=INPUT_FILE,
                  timeframe=bt.TimeFrame.Minutes,
                  nullvalue=0.0,
                  openinterest=-1)

    # Parse from/to-date
    dtfmt, tmfmt = '%Y-%m-%d', 'T%H:%M:%S'
    for a, d in ((getattr(args, x), x) for x in ['fromdate', 'todate']):
        if a:
            strpfmt = dtfmt + tmfmt * ('T' in a)
            kwargs[d] = datetime.datetime.strptime(a, strpfmt)

    cerebro = bt.Cerebro()  # create a "Cerebro" engine instance

    # cal = bt.TradingCalendar
    # cerebro.addcalendar(cal)

    data = BitcoinFeed(**kwargs)

    cerebro.broker.set_coc(True)

    cerebro.adddata(data)  # Add the data feed

    broker_kwargs = dict(coc=True)
    cerebro.broker = bt.brokers.BackBroker(**broker_kwargs)

    cerebro.broker.set_cash(100.0)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)

    cerebro.addstrategy(Strategy, agent=agent)  # Add the trading strategy
    # cerebro.addstrategy(Strategy)  # Add the trading strategy

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()  # run it all

    print('finish Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()  # plot


def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Backtrader Basic Script'
        )
    )

    parser.add_argument('--dargs', required=False, default='',
                        metavar='kwargs', help='kwargs in key=value format')

    # Defaults for dates
    parser.add_argument('--fromdate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    parser.add_argument('--todate', required=False, default='',
                        help='Date[time] in YYYY-MM-DD[THH:MM:SS] format')

    return parser.parse_args(pargs)


if __name__ == '__main__':
    run()
