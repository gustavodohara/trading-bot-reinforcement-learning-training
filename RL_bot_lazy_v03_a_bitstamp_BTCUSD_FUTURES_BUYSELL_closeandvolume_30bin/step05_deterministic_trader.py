import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import os
import argparse
from datetime import datetime
import pickle

from utils import get_data, maybe_make_dir
from agent import Agent
from environment import Env
from state_mapper import StateMapper

INPUT_FILE = '../data/bitstamp_btc_usd_only_Timestamp_and_close_price_and_volume_30m.csv'
feats = ['BTC']
feats_to_print = feats


def play_one_episode(agent, env, is_train):
    state = env.reset()
    done = False
    total_reward = 0
    actions = []

    while not done:
        action = agent.act(state)
        timestamp = env.df.index[env.current_idx]
        print(f"append action: ({env.current_idx}) time {timestamp} action {action} state{state}")
        actions.append((timestamp, action))
        next_state, reward, done = env.step(action)
        total_reward += reward
        # no training just DO!
        # if is_train:
        #     agent.train(state, action, reward, next_state, done)
        state = next_state

    print(f"last state{state}")

    return (total_reward, actions)


if __name__ == '__main__':

    # config
    models_folder = 'q_learning_rl_trader_models'
    actions_folder = 'q_learning_rl_trader_actions'
    num_episodes = 1

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, required=True,
                        help='either "train" or "test"')
    args = parser.parse_args()

    maybe_make_dir(models_folder)
    maybe_make_dir(actions_folder)

    df_returns = get_data(INPUT_FILE)

    print(df_returns[feats_to_print].head())

    # split into train (80%) and test (20%)
    Ntest = len(df_returns.index) // 5
    train_data = df_returns.iloc[:-Ntest]
    test_data = df_returns.iloc[-Ntest:]

    env = Env(train_data)
    action_size = len(env.action_space)
    state_mapper = StateMapper(env)
    # then load previous state_mapper
    state_mapper.load(f'{models_folder}/state_mapper.pkl')

    # If epsilon is 0 then is deterministics (the rewards are always the same!)
    agent = Agent(action_size, state_mapper, epsilon=0.00)
    print(state_mapper.bins)
    is_train = True

    # load trained weights
    agent.load(f'{models_folder}/q.pkl')

    if args.mode == 'test':
        is_train = False

        # remake the env with test data
        env = Env(test_data)

    # rewards = np.empty(num_episodes)

    t0 = datetime.now()
    r, actions = play_one_episode(agent, env, is_train=is_train)
    dt = datetime.now() - t0
    # rewards[e] = r

    # print(f"eps: {e + 1}/{num_episodes}, reward: {r:.5f}, duration: {dt} ")
    # print(f"actions", actions)

    # save actions and time
    a_file = open(f'{actions_folder}/{args.mode}.npy', "wb")
    pickle.dump(actions, a_file)
    a_file.close()

    # save the weights when we are done
    # if args.mode == 'train':
    # # save the Q
    # agent.save(f'{models_folder}/q.pkl')
    #
    # # save the state_mapper
    # state_mapper.save(f'{models_folder}/state_mapper.pkl')

    # save portfolio value for each episode
    # np.save(f'{rewards_folder}/{args.mode}.npy', rewards)

    # print('rewards', rewards)
