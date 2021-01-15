import numpy as np
import pickle


class Agent:
    def __init__(self, action_size, state_mapper, epsilon=0.1):
        self.action_size = action_size
        self.gamma = 0.8  # discount rate
        self.epsilon = epsilon
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
