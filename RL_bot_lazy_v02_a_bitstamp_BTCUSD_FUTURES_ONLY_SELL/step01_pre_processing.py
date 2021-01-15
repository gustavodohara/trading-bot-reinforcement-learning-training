# we have a file with open/High/Low/Close prices, we only want a open price
# if the file exist do nothing

import pandas as pd
import os.path
import sys

INPUT_FILE = '../data/bitstamp-BTC-USD_30m_dic14-dic20.csv'
OUTPUT_FILE = '../data/bitstamp_btc_usd_only_Timestamp_and_close_price_30m.csv'


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
btc_usdt_df.drop(['Open', 'High', 'Low', 'Volume'], 'columns', inplace=True)

# rename column to BTC
btc_usdt_df.rename(columns={'Close': 'BTC'}, inplace=True)

print(btc_usdt_df.head())

btc_usdt_df.to_csv(OUTPUT_FILE, index=False)
