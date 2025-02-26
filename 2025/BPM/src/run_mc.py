import numpy as np
import pandas as pd
from model import run_bpm_model, Params
from mc_params import *

def monte_carlo_simulation(params):
    num_simulations = params.num_simulations

    results = []

    for i in range(num_simulations):
        # Sample parameters from distributions
        # If you add more parameters, remember to also add a draw below:
        params.V = params.V_dist.rvs()

        # Run the model with sampled parameters
        f, spl_p, spl_s = run_bpm_model(params)

        # Store the results
        for j in range(len(f)):
            results.append({
                'simulation_id': i + 1,
                'frequency': f[j],
                'spl_p': spl_p[j],
                'spl_s': spl_s[j]
            })

    return pd.DataFrame(results)

if __name__ == "__main__":
    # Create a Params object with default values
    params = Params(**vars())
    # Run the Monte Carlo simulation
    results = monte_carlo_simulation(params)
    # Save the results to a CSV file
    results.to_csv('{params.outputfilename}.csv', index=False)
