import numpy as np
import pandas as pd
from itertools import product
from model import run_bpm_model, Params
from base_params import *

def single_simulation(params):
    results = []
    for v, alpha in product(params.V, params.alpha):
        params.V = v
        params.alpha = alpha
        f, spl_p, spl_s = run_bpm_model(params)
        for i in range(len(f)):
            results.append({
                'velocity': v,
                'alpha': alpha,
                'frequency': f[i],
                'spl_p': spl_p[i],
                'spl_s': spl_s[i]
            })
    return pd.DataFrame(results)

if __name__ == "__main__":
    # Create a Params object with default values
    params = Params(**vars())

    # Run a single simulation
    results = single_simulation(params)
    results.to_csv(f'{params.outputfilename}.csv', index=False)

