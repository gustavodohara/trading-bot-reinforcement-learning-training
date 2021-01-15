import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import argparse
import numpy as np
import pickle

INPUT_FILE = '../data/bitstamp_btc_usd_only_Timestamp_and_close_price_30m.csv'
feats = ['BTC']
feats_to_print = feats
actions_folder = 'q_learning_rl_trader_actions'


def get_data():
    df0 = pd.read_csv(INPUT_FILE, parse_dates=True)
    df_returns = pd.DataFrame()

    df_returns['Timestamp'] = df0['Timestamp']
    df_returns['log_return'] = np.log(df0['BTC']).diff()
    df_returns['close'] = df0['BTC']

    print(df_returns.head())

    return df_returns


parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type=str, required=True,
                    help='either "train" or "test"')
args = parser.parse_args()

df_returns = get_data()

# split into train (80%) and test (20%)
Ntest = len(df_returns.index) // 5
train_data = df_returns.iloc[:-Ntest]
test_data = df_returns.iloc[-Ntest:]

df_market_data = train_data

if args.mode == 'test':
    df_market_data = test_data

# trace_close = go.Scatter(x=df_market_data['Timestamp'], y=df_market_data['close'], name='BTC')
# layout = go.Layout(title='BTC Price', plot_bgcolor='rgb(230, 230, 230)', showlegend=True)


a_file = open(f'{actions_folder}/{args.mode}.npy', "rb")
a = pickle.load(a_file)
df_actions = pd.DataFrame(a, columns=['Timestamp', 'action'])
df_market_data_no_timestamp = df_market_data.drop(['Timestamp'], 'columns').reset_index(drop=True)
df_actions_close = pd.concat([df_actions, df_market_data_no_timestamp], axis=1, sort=False)
print(df_actions_close.head())

trace_actions = go.Scatter(x=df_actions['Timestamp'], y=df_actions['action'], name='actions')
fig = px.scatter(df_actions_close, x='Timestamp', y='close', text='action', log_x=True, size_max=60)
fig.update_traces(textposition='top center')
fig.update_layout(
    height=800,
    title_text='GDP and Life Expectancy (Americas, 2007)'
)

trace_close = go.Scatter(x=df_actions_close['Timestamp'], y=df_actions_close['close'], name='BTC')
df_actions_buy = df_actions_close[df_actions_close['action'] == 0]
df_actions_sell = df_actions_close[df_actions_close['action'] == 1]
df_actions_hold = df_actions_close[df_actions_close['action'] == 2]
trace_buy = go.Scatter(x=df_actions_buy['Timestamp'], y=df_actions_buy['close'], name='BUY', mode='markers',
                       marker={
                           'size': 12,
                           'color': 'green',
                           'line': {'width': 2, 'color': 'DarkSlateGrey'},
                           'symbol': 'triangle-up'})
trace_sell = go.Scatter(x=df_actions_sell['Timestamp'], y=df_actions_sell['close'], name='SELL', mode='markers',
                        marker={
                            'size': 12,
                            'color': 'red',
                            'line': {'width': 2, 'color': 'DarkSlateGrey'},
                            'symbol': 'triangle-down'})
# trace_hold = go.Scatter(x=df_actions_buy['Timestamp'], y=df_actions_hold['close'], name='HOLD', mode='markers',
#                         marker={
#                             'size': 12,
#                             'color': 'green',
#                             'line': {'width': 2, 'color': 'DarkSlateGrey'},
#                             'symbol': 'triangle-up'})
layout = go.Layout(title='BTC Price', plot_bgcolor='rgb(230, 230, 230)', showlegend=True)

data = [trace_close, trace_buy, trace_sell]

fig = go.Figure(data=data, layout=layout)

fig.show()
