import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import os
import argparse
from datetime import datetime
import pickle

INPUT_FILE = '../data/binance_btc_usdt_only_Timestamp_and_close_price_30m.csv'
feats = ['BTC']
feats_to_print = feats


def get_data():
    df0 = pd.read_csv(INPUT_FILE, index_col=0, parse_dates=True)
    df0.dropna(axis=0, how='all', inplace=True)
    df0.dropna(axis=1, how='any', inplace=True)

    df_returns = pd.DataFrame()
    for name in df0.columns:
        df_returns[name] = np.log(df0[name]).diff()

    print(df_returns.head())

    return df_returns


def maybe_make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class Env:
    def __init__(self, df):
        self.df = df
        self.n = len(df)
        self.current_idx = 0
        self.action_space = [0, 1, 2]  # BUY, SELL, HOLD
        self.invested = 0

        self.states = self.df[feats].to_numpy()
        # ahora el reward esta en la columna BTC
        # Tanto los estados como los returns son la misma columna BTC (log return)
        self.rewards = self.df['BTC'].to_numpy()
        self.total_buy_and_hold = 0

    def reset(self):
        self.current_idx = 0
        self.total_buy_and_hold = 0
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
        else:
            reward = 0

        # state transition
        next_state = self.states[self.current_idx]

        # baseline
        self.total_buy_and_hold += self.rewards[self.current_idx]

        done = (self.current_idx == self.n - 1)
        return next_state, reward, done


# aca definimos los "bins" para convertur algo continuo e infinito (log_returns) en algo discreto y finito
# la idea de esto es convertir un vector continuo de estados al bin correcto
class StateMapper:
    # vamos a recorrer por el environment de forma random para recolectar samples (unas 10.000 veces)
    def __init__(self, env, n_bins=6, n_samples=10000):
        # first, collect sample states from the environment
        states = []
        done = False
        s = env.reset()
        self.D = len(s)  # number of elements we need to bin
        states.append(s)
        for _ in range(n_samples):
            a = np.random.choice(env.action_space)
            s2, _, done = env.step(a)
            states.append(s2)
            if done:
                s = env.reset()
                states.append(s)

        # convert to numpy array for easy indexing
        states = np.array(states)

        # create the bins for each dimension
        self.bins = []
        # self.D es cada una de las columnas (o acciones)
        for d in range(self.D):
            column = np.sort(states[:, d])

            # find the boundaries for each bin
            current_bin = []
            for k in range(n_bins):
                # esto nos asegura de centrar los limites de los bin (chequear)
                boundary = column[int(n_samples / n_bins * (k + 0.5))]
                current_bin.append(boundary)

            self.bins.append(current_bin)

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

    def save(self, filepath):
        # print(f"saving bins of type {type(self.bins)}")
        # np.savez_compressed(filepath, self.bins)

        print(f"saving bins {self.bins}")

        a_file = open(filepath, "wb")
        pickle.dump(self.bins, a_file)
        a_file.close()


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

    df_returns = get_data()

    print(df_returns[feats_to_print].head())

    # split into train and test
    Ntest = 11000
    train_data = df_returns.iloc[:-Ntest]
    test_data = df_returns.iloc[-Ntest:]

    env = Env(train_data)
    action_size = len(env.action_space)
    state_mapper = StateMapper(env)
    agent = Agent(action_size, state_mapper)
    print(state_mapper.bins)
    is_train = True

    # then load previous state_mapper
    state_mapper.load(f'{models_folder}/state_mapper.pkl')

    # If epsilon is 0 then is deterministics (the rewards are always the same!)
    agent.epsilon = 0.00

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
