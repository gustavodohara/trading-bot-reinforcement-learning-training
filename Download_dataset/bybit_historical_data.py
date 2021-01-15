# this code is based on get_historical_data() from python-binance module
# https://github.com/sammchardy/python-binance
# it also requires pybybit.py available from this page
# https://note.mu/mtkn1/n/n9ef3460e4085
# (where pandas & websocket-client are needed)

import time
import dateparser
import pytz
import json
import csv
import pandas as pd
from datetime import datetime

import hashlib
import hmac

import urllib.parse
from threading import Thread
from collections import deque

from pathlib import Path

from requests import Request, Session
from requests.exceptions import HTTPError
from websocket import WebSocketApp


def load_config_exchange():
    with open('../config/exchange_params.json', 'r') as f:
        params = json.load(f)

    # Create our store
    config = {'apiKey': params["bybit"]["apikey"],
              'secret': params["bybit"]["secret"],
              'enableRateLimit': True,
              }

    return config


class Bybit():
    url_main = 'https://api.bybit.com'
    url_test = 'https://api-testnet.bybit.com'
    ws_url_main = 'wss://stream.bybit.com/realtime'
    ws_url_test = 'wss://stream-testnet.bybit.com/realtime'
    headers = {'Content-Type': 'application/json'}

    def __init__(self, api_key, secret, symbol, ws=True, test=False):
        self.api_key = api_key
        self.secret = secret

        self.symbol = symbol
        self.s = Session()
        self.s.headers.update(self.headers)

        self.url = self.url_main if not test else self.url_test
        self.ws_url = self.ws_url_main if not test else self.ws_url_test

        self.ws = ws
        if ws:
            self._connect()

    #
    # WebSocket
    #

    def _connect(self):
        self.ws = WebSocketApp(url=self.ws_url,
                               on_open=self._on_open,
                               on_message=self._on_message)

        self.ws_data = {'trade.' + str(self.symbol): deque(maxlen=200),
                        'instrument.' + str(self.symbol): {},
                        'order_book_25L1.' + str(self.symbol): pd.DataFrame(),
                        'position': {},
                        'execution': deque(maxlen=200),
                        'order': deque(maxlen=200)
                        }

        # 初期ポジション取得
        positions = self.get_position_http()['result']
        for p in positions:
            if p['symbol'] == self.symbol:
                self.ws_data['position'].update(p)
                break

        # WS接続
        Thread(target=self.ws.run_forever, daemon=True).start()

    def _on_open(self):
        timestamp = int(time.time() * 1000)
        param_str = 'GET/realtime' + str(timestamp)
        sign = hmac.new(self.secret.encode('utf-8'),
                        param_str.encode('utf-8'), hashlib.sha256).hexdigest()

        self.ws.send(json.dumps(
            {'op': 'auth', 'args': [self.api_key, timestamp, sign]}))
        self.ws.send(json.dumps(
            {'op': 'subscribe', 'args': ['trade.' + str(self.symbol),
                                         'instrument.' + str(self.symbol),
                                         'order_book_25L1.' + str(self.symbol),
                                         'position',
                                         'execution',
                                         'order']}))

    def _on_message(self, message):
        message = json.loads(message)
        topic = message.get('topic')
        # 各トピックごとの処理
        if topic == 'order_book_25L1.' + str(self.symbol):
            if message['type'] == 'snapshot':
                self.ws_data[topic] = pd.io.json.json_normalize(message['data']).set_index('id').sort_index(
                    ascending=False)
            else:  # message['type'] == 'delta'
                # delete or update or insert
                if len(message['data']['delete']) != 0:
                    drop_list = [x['id'] for x in message['data']['delete']]
                    self.ws_data[topic].drop(index=drop_list)
                elif len(message['data']['update']) != 0:
                    update_list = pd.io.json.json_normalize(message['data']['update']).set_index('id')
                    self.ws_data[topic].update(update_list)
                    self.ws_data[topic] = self.ws_data[topic].sort_index(ascending=False)
                elif len(message['data']['insert']) != 0:
                    insert_list = pd.io.json.json_normalize(message['data']['insert']).set_index('id')
                    self.ws_data[topic].update(insert_list)
                    self.ws_data[topic] = self.ws_data[topic].sort_index(ascending=False)

        elif topic in ['trade.' + str(self.symbol), 'execution', 'order']:
            # dequeにappendするだけ
            self.ws_data[topic].append(message['data'][0])

        elif topic in ['instrument.' + str(self.symbol), 'position']:
            # 辞書を上書きするだけ
            self.ws_data[topic].update(message['data'][0])

    def get_trade(self):
        """
        約定履歴を取得
        """
        if not self.ws: return None

        return self.ws_data['trade.' + str(self.symbol)]

    def get_instrument(self):
        """
        ティッカー情報を取得
        """
        if not self.ws: return None

        # データ待ち
        while len(self.ws_data['instrument.' + str(self.symbol)]) != 4:
            time.sleep(1.0)

        return self.ws_data['instrument.' + str(self.symbol)]

    def get_orderbook(self, side=None):
        """
        板情報を取得する
        sideに'Sell'または'Buy'を指定可能
        ※データ型: Pandas DataFrame形式
        """
        if not self.ws: return None

        # データ待ち
        while self.ws_data['order_book_25L1.' + str(self.symbol)].empty:
            time.sleep(1.0)

        if side == 'Sell':
            orderbook = self.ws_data['order_book_25L1.' + str(self.symbol)].query('side.str.contains("Sell")',
                                                                                  engine='python')
        elif side == 'Buy':
            orderbook = self.ws_data['order_book_25L1.' + str(self.symbol)].query('side.str.contains("Buy")',
                                                                                  engine='python')
        else:
            orderbook = self.ws_data['order_book_25L1.' + str(self.symbol)]
        return orderbook

    def get_position(self):
        """
        ポジションを取得
        """
        if not self.ws: return None

        return self.ws_data['position']

    def get_my_executions(self):
        """
        アカウントの約定履歴を取得
        """
        if not self.ws: return None

        return self.ws_data['execution']

    def get_order(self):
        """
        オーダー情報を取得
        """
        if not self.ws: return None

        return self.ws_data['order']

    #
    # Http Apis
    #

    def _request(self, method, path, payload):
        payload['api_key'] = self.api_key
        payload['timestamp'] = int(time.time() * 1000)
        payload = dict(sorted(payload.items()))
        for k, v in list(payload.items()):
            if v is None:
                del payload[k]

        param_str = urllib.parse.urlencode(payload)
        sign = hmac.new(self.secret.encode('utf-8'),
                        param_str.encode('utf-8'), hashlib.sha256).hexdigest()
        payload['sign'] = sign

        if method == 'GET':
            query = payload
            body = None
        else:
            query = None
            body = json.dumps(payload)

        req = Request(method, self.url + path, data=body, params=query)
        prepped = self.s.prepare_request(req)

        resp = None
        try:
            resp = self.s.send(prepped)
            resp.raise_for_status()
        except HTTPError as e:
            print(e)

        try:
            return resp.json()
        except json.decoder.JSONDecodeError as e:
            print('json.decoder.JSONDecodeError: ' + str(e))
            return resp.text

    def place_active_order(self, side=None, symbol=None, order_type=None,
                           qty=None, price=None,
                           time_in_force='GoodTillCancel', take_profit=None,
                           stop_loss=None, order_link_id=None):
        """
        オーダーを送信
        """
        payload = {
            'side': side,
            'symbol': symbol if symbol else self.symbol,
            'order_type': order_type,
            'qty': qty,
            'price': price,
            'time_in_force': time_in_force,
            'take_profit': take_profit,
            'stop_loss': stop_loss,
            'order_link_id': order_link_id
        }
        return self._request('POST', '/open-api/order/create', payload=payload)

    def get_active_order(self, order_id=None, order_link_id=None, symbol=None,
                         sort=None, order=None, page=None, limit=None,
                         order_status=None):
        """
        オーダーを取得
        """
        payload = {
            'order_id': order_id,
            'order_link_id': order_link_id,
            'symbol': symbol if symbol else self.symbol,
            'sort': sort,
            'order': order,
            'page': page,
            'limit': limit,
            'order_status': order_status
        }
        return self._request('GET', '/open-api/order/list', payload=payload)

    def cancel_active_order(self, order_id=None):
        """
        オーダーをキャンセル
        """
        payload = {
            'order_id': order_id
        }
        return self._request('POST', '/open-api/order/cancel', payload=payload)

    def place_conditional_order(self, side=None, symbol=None, order_type=None,
                                qty=None, price=None, base_price=None,
                                stop_px=None, time_in_force='GoodTillCancel',
                                close_on_trigger=None, reduce_only=None,
                                order_link_id=None):
        """
        条件付きオーダーを送信
        """
        payload = {
            'side': side,
            'symbol': symbol if symbol else self.symbol,
            'order_type': order_type,
            'qty': qty,
            'price': price,
            'base_price': base_price,
            'stop_px': stop_px,
            'time_in_force': time_in_force,
            'close_on_trigger': close_on_trigger,
            'reduce_only': reduce_only,
            'order_link_id': order_link_id
        }
        return self._request('POST', '/open-api/stop-order/create', payload=payload)

    def get_conditional_order(self, stop_order_id=None, order_link_id=None,
                              symbol=None, sort=None, order=None, page=None,
                              limit=None):
        """
        条件付きオーダーを取得
        """
        payload = {
            'stop_order_id': stop_order_id,
            'order_link_id': order_link_id,
            'symbol': symbol if symbol else self.symbol,
            'sort': sort,
            'order': order,
            'page': page,
            'limit': limit
        }
        return self._request('GET', '/open-api/stop-order/list', payload=payload)

    def cancel_conditional_order(self, order_id=None):
        """
        条件付きオーダーをキャンセル
        """
        payload = {
            'order_id': order_id
        }
        return self._request('POST', '/open-api/stop-order/cancel', payload=payload)

    def get_leverage(self):
        """
        レバレッジを取得
        """
        payload = {}
        return self._request('GET', '/user/leverage', payload=payload)

    def change_leverage(self, symbol=None, leverage=None):
        """
        レバレッジを変更
        """
        payload = {
            'symbol': symbol if symbol else self.symbol,
            'leverage': leverage
        }
        return self._request('POST', '/user/leverage/save', payload=payload)

    def get_position_http(self):
        """
        ポジションを取得(HTTP版)
        """
        payload = {}
        return self._request('GET', '/position/list', payload=payload)

    def change_position_margin(self, symbol=None, margin=None):
        """
        ポジションマージンを変更
        """
        payload = {
            'symbol': symbol if symbol else self.symbol,
            'margin': margin
        }
        return self._request('POST', '/position/change-position-margin', payload=payload)

    def get_prev_funding_rate(self, symbol=None):
        """
        ファンディングレートを取得
        """
        payload = {
            'symbol': symbol if symbol else self.symbol,
        }
        return self._request('GET', '/open-api/funding/prev-funding-rate', payload=payload)

    def get_prev_funding(self, symbol=None):
        """
        アカウントのファンディングレートを取得
        """
        payload = {
            'symbol': symbol if symbol else self.symbol,
        }
        return self._request('GET', '/open-api/funding/prev-funding', payload=payload)

    def get_predicted_funding(self, symbol=None):
        """
        予測資金調達レートと資金調達手数料を取得
        """
        payload = {
            'symbol': symbol if symbol else self.symbol,
        }
        return self._request('GET', '/open-api/funding/predicted-funding', payload=payload)

    def get_my_execution(self, order_id=None):
        """
        アカウントの約定情報を取得
        """
        payload = {
            'order_id': order_id
        }
        return self._request('GET', '/v2/private/execution/list', payload=payload)

    #
    # New Http Apis (developing)
    #

    def symbols(self):
        """
        シンボル情報を取得
        """
        payload = {}
        return self._request('GET', '/v2/public/symbols', payload=payload)

    def kline(self, symbol=None, interval=None, _from=None, limit=None):
        """
        ローソク足を取得 (developing)
        """
        payload = {
            'symbol': symbol if symbol else self.symbol,
            'interval': interval,
            'from': _from,
            'limit': limit
        }
        return self._request('GET', '/v2/public/kline/list', payload=payload)

    def place_active_order_v2(self, symbol=None, side=None, order_type=None,
                              qty=None, price=None,
                              time_in_force='GoodTillCancel',
                              order_link_id=None):
        """
        オーダーを送信 v2 (developing)
        """
        payload = {
            'symbol': symbol if symbol else self.symbol,
            'side': side,
            'order_type': order_type,
            'qty': qty,
            'price': price,
            'time_in_force': time_in_force,
            'order_link_id': order_link_id
        }
        return self._request('POST', '/v2/private/order/create', payload=payload)

    def cancel_active_order_v2(self, order_id=None):
        """
        オーダーをキャンセル v2 (developing)
        """
        payload = {
            'order_id': order_id
        }
        return self._request('POST', '/v2/private/order/cancel', payload=payload)


exchange_config = load_config_exchange()

bybit = bybit = Bybit(api_key=exchange_config['apiKey'],
                      secret=exchange_config['secret'], symbol='BTCUSD', test=True, ws=True)


def date_to_milliseconds(date):
    # FROM = '2017-01-0100:00:00Z
    if date == 'now':
        utc_time = datetime.utcnow()
    else:
        utc_time = datetime.strptime(date, "%Y-%m-%d%H:%M:%SZ")

    # milliseconds = (utc_time - datetime(1970, 1, 1))
    milliseconds = utc_time.timestamp() * 1000
    return milliseconds


def datetime_to_datestring(my_datetime):
    date = datetime.fromtimestamp(my_datetime)
    # return date.strptime(str(datetime), '%Y-%m-%d %H:%M:%S')

    return date.strftime('%Y-%m-%d %H:%M:%S.%d')

def convert_time(my_datetime):
    newtime = datetime.fromtimestamp(my_datetime)
    # print("convertime", timestamp, "newtime", newtime)
    return newtime


def get_historical_klines(symbol, interval, start_str, end_str=None):
    """Get Historical Klines from Bybit

    See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

    If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    :param symbol: Name of symbol pair -- BTCUSD, ETCUSD, EOSUSD, XRPUSD
    :type symbol: str
    :param interval: Bybit Kline interval -- 1 3 5 15 30 60 120 240 360 720 "D" "M" "W" "Y"
    :type interval: str
    :param start_str: Start date string in UTC format
    :type start_str: str
    :param end_str: optional - end date string in UTC format
    :type end_str: str

    :return: list of OHLCV values

    """

    # set parameters for kline()
    timeframe = str(interval)
    limit = 200
    start_ts = int(date_to_milliseconds(start_str) / 1000)
    end_ts = None
    if end_str:
        end_ts = int(date_to_milliseconds(end_str) / 1000)
    else:
        end_ts = int(date_to_milliseconds('now') / 1000)

    # init our list
    output_data = []

    # loop counter
    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 200 entries
        temp_dict = bybit.kline(symbol=symbol, interval=timeframe, _from=start_ts, limit=limit)

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_dict):
            symbol_existed = True

        if symbol_existed:
            # extract data and convert to list
            temp_data = [list(i.values())[2:] for i in temp_dict['result']]
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            # NOTE: current implementation ignores inteval of D/W/M/Y  for now
            start_ts = temp_data[len(temp_data) - 1][0] + interval * 60

        else:
            # it wasn't listed yet, increment our start date
            start_ts += timeframe

        idx += 1

        print(len(temp_data), symbol, 'candles in total from', datetime_to_datestring(start_ts), 'to')

        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break

        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(0.2)

    return output_data


def get_historical_klines_pd(symbol, interval, start_str, end_str=None):
    """Get Historical Klines from Bybit

    See dateparse docs for valid start and end string formats
    http://dateparser.readthedocs.io/en/latest/

    If using offset strings for dates add "UTC" to date string
    e.g. "now UTC", "11 hours ago UTC"

    :param symbol: Name of symbol pair -- BTCUSD, ETCUSD, EOSUSD, XRPUSD
    :type symbol: str
    :param interval: Bybit Kline interval -- 1 3 5 15 30 60 120 240 360 720 "D" "M" "W" "Y"
    :type interval: str
    :param start_str: Start date string in UTC format
    :type start_str: str
    :param end_str: optional - end date string in UTC format
    :type end_str: str

    :return: list of OHLCV values

    """

    # set parameters for kline()
    timeframe = str(interval)
    limit = 200
    start_ts = int(date_to_milliseconds(start_str) / 1000)
    end_ts = None
    if end_str:
        end_ts = int(date_to_milliseconds(end_str) / 1000)
    else:
        end_ts = int(date_to_milliseconds('now') / 1000)

    # init our list
    output_data = []

    # loop counter
    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 200 entries
        temp_dict = bybit.kline(symbol=symbol, interval=timeframe, _from=start_ts, limit=limit)

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_dict):
            symbol_existed = True

        if symbol_existed:
            # extract data and convert to list
            temp_data = [list(i.values())[2:] for i in temp_dict['result']]
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            # NOTE: current implementation does not support inteval of D/W/M/Y
            start_ts = temp_data[len(temp_data) - 1][0] + interval * 60

        else:
            # it wasn't listed yet, increment our start date
            start_ts += timeframe

        print(len(temp_data), symbol, 'candles in total from', datetime_to_datestring(start_ts), 'to')

        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break

        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(0.2)

    # convert to data frame
    df = pd.DataFrame(output_data, columns=['TimeStamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'TurnOver'])
    df['Date'] = [datetime.fromtimestamp(i).strftime('%Y-%m-%dT%H:%M:%S.%d')[:-3] for i in df['TimeStamp']]

    return df


def write_to_csv(filename, exchange, df):
    p = Path("./data/raw/", str(exchange))
    p.mkdir(parents=True, exist_ok=True)
    full_path = p / str(filename)
    df.to_csv(full_path, index=False)


def parse_candles(data):
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(data, columns=header)
    df['Timestamp'] = df.apply(lambda x: convert_time(x['Timestamp']), axis=1)
    df = df.set_index('Timestamp')
    return df


def parse_dataframe(data_df):
    # format date
    # data_df['TimeStamp'] = pd.to_datetime(data_df['TimeStamp']).dt.strftime('%Y-%m-%dT%H:%M:%S')

    data_df.drop(['TimeStamp', 'TurnOver'], 'columns', inplace=True)

    # rename column
    data_df.rename(columns={'Date': 'TimeStamp'}, inplace=True)

    # reorder
    cols = data_df.columns.tolist()
    cols = cols[-1:] + cols[:-1]

    data_df = data_df[cols]

    return data_df


# def scrape_candles_to_csv(filename, symbol, interval, since, end_str=None):
#     ohlcv = get_historical_klines(symbol, interval, since, end_str)
#     # convert to panda dataframe
#     ohlcv_df = parse_candles(ohlcv)
#     # save them to csv file
#     write_to_csv(filename, 'bybit', ohlcv_df)
#     print('Saved', len(ohlcv_df), 'candles from', since, 'to now', 'to', filename)

def scrape_candles_to_csv(filename, symbol, interval, since, end_str=None):
    ohlcv_df = get_historical_klines_pd(symbol, interval, since, end_str)

    df_parsed = parse_dataframe(ohlcv_df)
    # save them to csv file
    write_to_csv(filename, 'bybit', df_parsed)
    print('Saved', len(df_parsed), 'candles from', since, 'to now', 'to', filename)


EXCHANGE = 'bybit'
# EXCHANGE = 'binance'
SYMBOL = 'EOSUSD'
# TIMEFRAME = '30m'
# TIMEFRAME = '1d'
INTERVAL = 30
FROM = '2018-01-0100:00:00Z'
# FROM = '2020-01-0100:00:00Z'
# FROM = '2020-12-2000:00:00Z'
FILENAME = '{}-{}_{}.csv'.format(EXCHANGE, SYMBOL.replace('/', '-'), INTERVAL)

scrape_candles_to_csv(FILENAME, SYMBOL, INTERVAL, FROM, end_str=None)
