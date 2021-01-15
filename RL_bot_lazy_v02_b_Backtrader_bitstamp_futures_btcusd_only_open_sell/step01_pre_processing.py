# we have a file with open/High/Low/Close prices, we only want a open price
# the file is binance-BTC_USDT-30m.csv
# this script create a new file binance_btc_usdt_only_close_price_30m.csv
# if the file exist do nothing

import pandas as pd
import os.path
import sys

INPUT_FILE = '../data/bitstamp-BTC-USD_30m_dic14-dic20.csv'
OUTPUT_FILE = '../data/bitstamp_btc_usd_dic14-dic20_backtrader_30m.csv'


def check_file_exist(path):
    if os.path.isfile(path):
        print("File exist")
        return True
    else:
        print("File not exist")
        return False


# check fine output do not exist
if (check_file_exist(OUTPUT_FILE)):
    print("The file already exist")
    sys.exit()

btc_usdt_df = pd.read_csv(INPUT_FILE)

print(btc_usdt_df.head())

# delete all columns but close price
# btc_usdt_df.drop(['Open', 'High', 'Low', 'Volume'], 'columns', inplace=True)

# rename column to BTC
btc_usdt_df.rename(columns={'Timestamp': 'datetime'}, inplace=True)

# format date
btc_usdt_df['datetime'] = pd.to_datetime(btc_usdt_df['datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')

print(btc_usdt_df.head())

btc_usdt_df.to_csv(OUTPUT_FILE, index=False)
