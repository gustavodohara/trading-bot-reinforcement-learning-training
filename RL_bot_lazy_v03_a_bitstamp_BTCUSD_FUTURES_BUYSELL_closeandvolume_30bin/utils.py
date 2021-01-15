import pandas as pd
import numpy as np
import os

def get_data(input_file):
    df0 = pd.read_csv(input_file, index_col=0, parse_dates=True)
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