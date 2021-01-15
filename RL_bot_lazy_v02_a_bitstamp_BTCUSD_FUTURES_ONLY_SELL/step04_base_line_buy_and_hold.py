import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import os
import argparse
from datetime import datetime
import pickle

INPUT_FILE = '../data/bitstamp_btc_usd_only_Timestamp_and_close_price_30m.csv'

# usamos solo apple, microsoft y amazon
feats = ['BTC']
feats_rewards = ['return']


def get_data():
    df0 = pd.read_csv(INPUT_FILE, index_col=0, parse_dates=True)
    df0.dropna(axis=0, how='all', inplace=True)
    df0.dropna(axis=1, how='any', inplace=True)

    df_returns = pd.DataFrame()
    df_returns['BTC'] = df0['BTC']
    df_returns['log_return'] = np.log(df0['BTC']).diff()
    df_returns['return'] = df0['BTC'].diff()

    print(df_returns.head())

    return df_returns


def get_data_raw():
    df0 = pd.read_csv(INPUT_FILE, index_col=0, parse_dates=True)
    df0.dropna(axis=0, how='all', inplace=True)
    df0.dropna(axis=1, how='any', inplace=True)

    print('get_data_raw', df0.head())

    return df0

def print_train_and_test_date(df, n):
    train_data = df.iloc[:-n]
    test_data = df.iloc[-n:]
    # print("train_data from {} to {} ".format(train_data.iloc[0], train_data.iloc[-1]))
    print("x"*40)
    print("train_data from {} to {} ".format(train_data.iloc[0], train_data.iloc[-1]))
    print("test_data from {} to {} ".format(test_data.iloc[0], test_data.iloc[-1]))
    print("x" * 40)


class Env:
    def __init__(self, df):
        self.df = df
        self.n = len(df)
        self.current_idx = 0
        self.action_space = [0, 1, 2]  # BUY, SELL, HOLD
        self.invested = 0

        self.states = self.df[feats].to_numpy()
        # ahora el reward esta en la columna SPY
        self.rewards = self.df[feats_rewards].to_numpy()
        self.rewards_log_return = self.df['log_return'].to_numpy()
        self.total_buy_and_hold = 0
        self.total_log_return_buy_and_hold = 0

    def reset(self):
        self.current_idx = 0
        self.total_buy_and_hold = 0
        self.total_log_return_buy_and_hold = 0
        return self.states[self.current_idx]

    def step(self, action):
        # need to return (next_state, reward, done)

        self.current_idx += 1
        if self.current_idx >= self.n:
            raise Exception("Episode already done")

        if action == 0:  # BUY
            self.invested = 1
        elif action == 1:  # SELL
            self.invested = 0

        # compute reward
        if self.invested:
            reward = self.rewards[self.current_idx]
            reward_log_return = self.rewards_log_return[self.current_idx]
        else:
            reward = 0
            reward_log_return = 0

        # state transition
        next_state = self.states[self.current_idx]

        # baseline
        self.total_buy_and_hold += self.rewards[self.current_idx]
        self.total_log_return_buy_and_hold += self.rewards_log_return[self.current_idx]

        done = (self.current_idx == self.n - 1)
        return next_state, reward, done


def play_one_episode(env):
    state = env.reset()
    done = False
    total_reward = 0

    print('fist state', state)

    while not done:
        # buy and hold action
        action = 0  # agent BUY
        next_state, reward, done = env.step(action)
        total_reward += reward
        state = next_state
        if done:
            print('last state', state)

    return total_reward


if __name__ == '__main__':

    num_episodes = 1

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, required=True,
                        help='either "train" or "test"')
    args = parser.parse_args()

    df_returns = get_data()
    df_raw = get_data_raw()

    # split into train (80%) and test (20%)
    Ntest = len(df_returns.index) // 5
    print("buy and hold quantity test set", Ntest)
    train_data = df_returns.iloc[:-Ntest]
    test_data = df_returns.iloc[-Ntest:]
    print_train_and_test_date(df_raw, Ntest)

    env = Env(train_data)
    action_size = len(env.action_space)

    if args.mode == 'test':
        # remake the env with test data
        env = Env(test_data)

    rewards = np.empty(num_episodes)

    for e in range(num_episodes):
        t0 = datetime.now()
        r = play_one_episode(env)
        dt = datetime.now() - t0
        rewards[e] = r

    print(f"env.total_buy_and_hold {env.total_buy_and_hold}")
    print(f"reward {env.total_log_return_buy_and_hold}")
    print(f"percentage earn/loss {np.exp(env.total_log_return_buy_and_hold): .2f}%")
