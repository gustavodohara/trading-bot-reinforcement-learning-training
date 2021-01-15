import numpy as np
import itertools
import pickle


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
