import matplotlib.pyplot as plt
import numpy as np
import argparse

rewards_folder = 'q_learning_rl_trader_rewards'

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type=str, required=True,
                    help='either "train" or "test"')
args = parser.parse_args()

a = np.load(f'{rewards_folder}/{args.mode}.npy')

print(f"average reward: {a.mean():.2f}, min: {a.min():.2f}, max: {a.max():.2f}")
print(f"average percentage earn/loss: {np.exp(a.mean()):.2f}%, min: {np.exp(a.min()):.2f}%, max: {np.exp(a.max()):.2f}%")

if args.mode == 'train':
    # show the training progress
    plt.plot(a)
else:
    # test - show a histogram of rewards
    plt.hist(a, bins=20)

    # plt.plot(train_rewards, label="train")
    # plt.plot(test_rewards, label="test")
    # plt.legend()
    # plt.show()

plt.title(args.mode)
plt.show()
