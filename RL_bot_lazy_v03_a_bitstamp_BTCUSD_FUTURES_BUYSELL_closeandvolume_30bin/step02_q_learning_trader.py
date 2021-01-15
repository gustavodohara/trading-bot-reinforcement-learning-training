import numpy as np
import argparse
from datetime import datetime

from utils import get_data, maybe_make_dir
from agent import Agent
from environment import Env
from state_mapper import StateMapper

INPUT_FILE = '../data/bitstamp_btc_usd_only_Timestamp_and_close_price_and_volume_30m.csv'


# usamos solo apple, microsoft y amazon
feats = ['BTC', 'Volume']
feats_to_print = feats



def play_one_episode(agent, env, is_train):
    state = env.reset()
    done = False
    total_reward = 0
    action_stats = dict([(0, 0), (1, 0), (2, 0)])

    while not done:
        action = agent.act(state)
        action_stats[action] += 1
        next_state, reward, done = env.step(action)
        total_reward += reward
        if is_train:
            agent.train(state, action, reward, next_state, done)
        state = next_state

    return total_reward, action_stats


if __name__ == '__main__':

    # config
    models_folder = 'q_learning_rl_trader_models'
    rewards_folder = 'q_learning_rl_trader_rewards'
    num_episodes = 500
    n_bins = 30
    n_samples = 100000

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, required=True,
                        help='either "train" or "test"')
    args = parser.parse_args()

    maybe_make_dir(models_folder)
    maybe_make_dir(rewards_folder)

    df_returns = get_data(INPUT_FILE)

    print(df_returns[feats_to_print].head())

    # split into train (80%) and test (20%)
    Ntest = len(df_returns.index) // 5
    train_data = df_returns.iloc[:-Ntest]
    test_data = df_returns.iloc[-Ntest:]

    env = Env(train_data)
    action_size = len(env.action_space)
    state_mapper = StateMapper(env, n_bins, n_samples)
    agent = Agent(action_size, state_mapper)
    print(state_mapper.bins)
    is_train = True

    if args.mode == 'test':
        is_train = False
        # then load previous state_mapper
        state_mapper.load(f'{models_folder}/state_mapper.pkl')

        # remake the env with test data
        env = Env(test_data)

        # If epsilon is 0 then is deterministics (the rewards are alwais the same!)
        agent.epsilon = 0.01

        # load trained weights
        agent.load(f'{models_folder}/q.pkl')

    rewards = np.empty(num_episodes)

    for e in range(num_episodes):
        t0 = datetime.now()
        r, action_stats = play_one_episode(agent, env, is_train=is_train)
        dt = datetime.now() - t0
        rewards[e] = r

        print(
            f"eps: {e + 1}/{num_episodes}, reward: {r:.5f}, [BUY {action_stats[0]} SELL {action_stats[1]} HOLD {action_stats[2]}] duration: {dt} ")

    # save the weights when we are done
    if args.mode == 'train':
        # save the Q
        agent.save(f'{models_folder}/q.pkl')

        # save the state_mapper
        state_mapper.save(f'{models_folder}/state_mapper.pkl')

    # save portfolio value for each episode
    np.save(f'{rewards_folder}/{args.mode}.npy', rewards)
