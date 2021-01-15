from pathlib import Path

import csv
import ccxt
import os.path
from os import path

import pandas as pd


# -----------------------------------------------------------------------------

def retry_fetch_ohlcv(exchange, max_retries, symbol, timeframe, since, limit):
    num_retries = 0
    try:
        num_retries += 1
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        # print('Fetched', len(ohlcv), symbol, 'candles from', exchange.iso8601 (ohlcv[0][0]), 'to', exchange.iso8601 (ohlcv[-1][0]))
        return ohlcv
    except Exception:
        if num_retries > max_retries:
            raise  # Exception('Failed to fetch', timeframe, symbol, 'OHLCV in', max_retries, 'attempts')


def scrape_ohlcv(exchange, max_retries, symbol, timeframe, since, limit):
    earliest_timestamp = exchange.milliseconds()
    timeframe_duration_in_seconds = exchange.parse_timeframe(timeframe)
    timeframe_duration_in_ms = timeframe_duration_in_seconds * 1000
    timedelta = limit * timeframe_duration_in_ms
    all_ohlcv = []
    while True:
        fetch_since = earliest_timestamp - timedelta
        ohlcv = retry_fetch_ohlcv(exchange, max_retries, symbol, timeframe, fetch_since, limit)
        # if we have reached the beginning of history
        if ohlcv[0][0] >= earliest_timestamp:
            break
        earliest_timestamp = ohlcv[0][0]
        all_ohlcv = ohlcv + all_ohlcv
        print(len(all_ohlcv), symbol, 'candles in total from', exchange.iso8601(all_ohlcv[0][0]), 'to',
              exchange.iso8601(all_ohlcv[-1][0]))
        # if we have reached the checkpoint
        if fetch_since < since:
            break
    return all_ohlcv


# def write_to_csv(filename, exchange, data):
#     p = Path("./data/raw/", str(exchange))
#     p.mkdir(parents=True, exist_ok=True)
#     full_path = p / str(filename)
#     with Path(full_path).open('w+', newline='') as output_file:
#         csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         csv_writer.writerows(data)


def get_full_path_filename(filename, exchange):
    p = Path("./data/raw/", str(exchange))
    full_path = p / str(filename)
    return full_path

def write_to_csv(filename, exchange, df):
    p = Path("./data/raw/", str(exchange))
    p.mkdir(parents=True, exist_ok=True)
    full_path = p / str(filename)
    df.to_csv(full_path)


def convertTime(timestamp, exchange):
    newtime = exchange.iso8601(int(timestamp))
    # print("convertime", timestamp, "newtime", newtime)
    return newtime


def parse_candles(data, exchange):
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(data, columns=header)
    df['Timestamp'] = df.apply(lambda x: convertTime(x['Timestamp'], exchange), axis=1)
    df = df.set_index('Timestamp')
    return df


def scrape_candles_to_csv(filename, exchange_id, max_retries, symbol, timeframe, since, limit):
    # instantiate the exchange by id
    exchange = getattr(ccxt, exchange_id)({
        'enableRateLimit': True,  # required by the Manual
    })
    # convert since from string to milliseconds integer if needed
    if isinstance(since, str):
        since = exchange.parse8601(since)
    # preload all markets from the exchange
    exchange.load_markets()
    # fetch all candles
    ohlcv = scrape_ohlcv(exchange, max_retries, symbol, timeframe, since, limit)
    # convert to panda dataframe
    ohlcv_df = parse_candles(ohlcv, exchange)
    # save them to csv file
    write_to_csv(filename, exchange, ohlcv_df)
    print('Saved', len(ohlcv), 'candles from', exchange.iso8601(ohlcv[0][0]), 'to', exchange.iso8601(ohlcv[-1][0]),
          'to', filename)


def check_file_exist(filepath, exchange):
    full_path = get_full_path_filename(filepath, exchange)
    return path.exists(full_path)


def get_markets(exchange_id):
    # instantiate the exchange by id
    exchange = getattr(ccxt, exchange_id)({
        'enableRateLimit': True,  # required by the Manual
    })
    # preload all markets from the exchange
    return exchange.load_markets()


# EXCHANGE = 'bybit'
EXCHANGE = 'bitstamp'
# EXCHANGE = 'binance'
SYMBOL = 'BTC/USD'
# SYMBOL = 'ETH/USD'
TIMEFRAME = '15m'
# TIMEFRAME = '1d'
FROM = '2015-01-0100:00:00Z'
FILENAME = '{}-{}_{}.csv'.format(EXCHANGE, SYMBOL.replace('/', '-'), TIMEFRAME)


if check_file_exist(FILENAME, EXCHANGE):
    print("file already exist")
    exit(0)

scrape_candles_to_csv(FILENAME, EXCHANGE, 3, SYMBOL, TIMEFRAME, FROM, 1000)


# print(get_markets(EXCHANGE))
