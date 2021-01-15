import numpy as np
import itertools
import pickle


# aca definimos los "bins" para convertur algo continuo e infinito (log_returns) en algo discreto y finito
# la idea de esto es convertir un vector continuo de estados al bin correcto
class StateMapper:
    # vamos a recorrer por el environment de forma random para recolectar samples (unas 10.000 veces)
    def __init__(self, d):
        self.D = d  # number of elements we need to bin

        # create the bins for each dimension
        self.bins = []

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
