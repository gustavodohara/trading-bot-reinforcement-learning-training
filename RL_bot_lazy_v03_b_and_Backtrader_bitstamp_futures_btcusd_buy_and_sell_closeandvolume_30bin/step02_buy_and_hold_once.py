import datetime
import argparse
import backtrader as bt
import math

INPUT_FILE = '../data/bitstamp_btc_usd_dic14-dic20_backtrader_30m.csv'


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


# STRATEGY

class Strategy(bt.Strategy):

    def __init__(self):
        self.COIN = self.datas[0]

    def log(self, txt, dt=None):
        ''' Loggin function for this strategy'''
        datetime = self.datas[0].datetime
        date = datetime.date(0).isoformat()
        time = datetime.time()
        print('%s, %s, %s' % (date, time, txt))

    def start(self):
        self.val_start = self.broker.get_cash()  # keep the starting cash

    def nextstart(self):
        # Buy all the available cash
        size = self.broker.get_cash() / self.data
        size_truncated = math.floor(size * 100) / 100.0
        self.buy(size=size_truncated)

    def notify_order(self, order):
        if order.status not in [order.Completed]:
            return
        self.log('FIRST CLOSE %.2f' % (order.executed.price))

    def stop(self):
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        self.log('LAST CLOSE %.2f' % (self.datas[0].close[0]))
        print('ROI:        {:.2f}%'.format(100.0 * self.roi))


# RUN
def run(args=None):
    args = parse_args(args)

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

    data = BitcoinFeed(**kwargs)

    cerebro.broker.set_coc(True)

    cerebro.adddata(data)  # Add the data feed

    broker_kwargs = dict(coc=True)
    cerebro.broker = bt.brokers.BackBroker(**broker_kwargs)

    cerebro.broker.set_cash(100.0)

    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)

    cerebro.addstrategy(Strategy)  # Add the trading strategy

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
