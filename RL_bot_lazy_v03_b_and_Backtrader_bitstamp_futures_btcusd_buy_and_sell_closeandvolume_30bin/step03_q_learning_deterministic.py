import datetime
import argparse
import backtrader as bt
import math

from agent import Agent
from state_mapper import StateMapper

INPUT_FILE = '../data/bitstamp_btc_usd_dic14-dic20_backtrader_30m.csv'

ACTION_SPACE_BUY = 0
ACTION_SPACE_SELL = 1
ACTION_SPACE_HOLD = 2

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
        self.datavolume = self.datas[0].volume
        # Sentinel to None: new ordersa allowed
        self.orefs = list()
        self.val_start = 0
        self.val_start_month = 0
        self.month_stats = []

        self.sell_order = None
        self.buy_order = None

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

    def is_end_state(self, order):
        return order.status in [bt.Order.Completed, bt.Order.Margin, bt.Order.Rejected, bt.Order.Canceled]

    def notify_order(self, order):
        if order.status != order.Completed:
            print('{}: Order ref: {} / Type {} / Status {} / Price {}'.format(
                self.data.datetime.date(0),
                order.ref, 'Buy' * order.isbuy() or 'Sell',
                order.getstatusname(),
                order.price)
            )
            pass
        else:
            print('{}: Order ref: {} / Type {} / Price {} / Value {} / COMPLETED '.format(
                self.data.datetime.date(0),
                order.ref, 'Buy' * order.isbuy() or 'Sell',
                order.executed.price,
                order.executed.value
            ))
            pass

        if self.is_end_state(order):
            if self.buy_order and order.ref == self.buy_order.ref:
                self.buy_order = None
            elif self.sell_order and order.ref == self.sell_order.ref:
                self.sell_order = None

        if not order.alive() and order.ref in self.orefs:
            self.orefs.remove(order.ref)


    def get_state(self):
        log_return_close = round(math.log(self.dataclose[0]) - math.log(self.dataclose[-1]), 8)
        # volume can be 0, so it need to check volume greater than 0 because of the mat.log
        log_return_volume_curr = 0
        log_return_volume_prev = 0
        if self.datavolume[0] > 0:
            log_return_volume_curr = math.log(self.datavolume[0])
        if self.datavolume[-1]:
            log_return_volume_prev = math.log(self.datavolume[-1])
        log_return_volume = round(log_return_volume_curr - log_return_volume_prev, 8)
        # print('get_state log_return=', log_return_close, 'log_return_volume', log_return_volume)
        return [log_return_close, log_return_volume]


    def buy_all(self, asset):
        if self.getposition(asset).size == 0.0:
            size = self.broker.get_cash() / self.data
            o = self.buy(size=size)
            self.buy_order = o
            self.orefs.append(o.ref)
        elif self.getposition(asset).size < 0:
            # there is an open position (a sell position)
            size = self.getposition(asset).size
            o = self.buy(size=size)
            self.buy_order = o
            self.orefs.append(o.ref)

    def sell_all(self, asset):
        if self.getposition(asset).size == 0.0:
            # no position open first sell order
            size = self.broker.get_cash() / self.data
            o = self.sell(size=size)
            self.sell_order = o
            self.orefs.append(o.ref)
        elif self.getposition(asset).size > 0:
            # buy position open (close previous buy order)
            size = self.getposition(asset).size
            o = self.sell(size=size)
            self.sell_order = o
            self.orefs.append(o.ref)

    def next(self):
        if len(self) <= 1:
            return

        if self.orefs:
            return  # pending orders do nothing

        # the state is the log_return
        state = self.get_state()
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


def printTradeAnalysis(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    # Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total, 2)
    strike_rate = (total_won / total_closed) * 100
    # Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed, total_won, total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    # Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    # Print the rows
    print_list = [h1, r1, h2, r2]
    row_format = "{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('', *row))


def printSQN(analyzer):
    sqn = round(analyzer.sqn, 2)
    print('-' * 40)
    print('1.6 – 1.9 Below average')
    print('2.0 – 2.4 Average')
    print('2.5 – 2.9 Good')
    print('3.0 – 5.0 Excellent')
    print('5.1 – 6.9 Superb')
    print('7.0 – Holy Grail?')
    print('SQN: {}'.format(sqn))
    print('-' * 40)


# RUN
def run(args=None):
    args = parse_args(args)

    # config
    models_folder = 'q_learning_rl_trader_models'

    D = 2
    action_space = [ACTION_SPACE_BUY, ACTION_SPACE_SELL, ACTION_SPACE_HOLD]  # BUY, SELL, HOLD

    state_mapper = StateMapper(D)

    # then load previous state_mapper
    state_mapper.load(f'{models_folder}/state_mapper.pkl')

    action_size = len(action_space)
    agent = Agent(action_size, state_mapper)

    # If epsilon is 0 then is deterministic (the rewards are always the same!)
    agent.epsilon = 0.00

    # load trained weights
    agent.load(f'{models_folder}/q.pkl')

    print('state_mapper.bins', state_mapper.bins)

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

    # Add the analyzers we are interested in
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    strategies = cerebro.run()  # run it all
    first_strat = strategies[0]

    # print the analyzers
    printTradeAnalysis(first_strat.analyzers.ta.get_analysis())
    printSQN(first_strat.analyzers.sqn.get_analysis())

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
