import pandas as pd
import numpy as np
from tqdm import tqdm

from forest_fire.model import ForestFire

import warnings
warnings.filterwarnings('ignore')

def run_forest_fire_experiment(width, height, density, spatial_pattern, steps):
    model = ForestFire(width=width, height=height, density=density, spatial_pattern=spatial_pattern)
    for _ in range(steps):
        if not model.running:
            break
        model.step()
    results_df = model.datacollector.get_model_vars_dataframe()
    return results_df['Percentage Burned Out'].iloc[-1]

def repeatedExperiments(experiments, width, height, density, steps):
    patterns = ["Random", "Clustered", "Lines"]
    results = {pattern: [] for pattern in patterns}

    for experiment in range(experiments):
        for pattern in patterns:
            burned_percentage = run_forest_fire_experiment(width, height, density, pattern, steps)
            print("Experiment " + str(experiment) + " - Pattern " + str(pattern) + ": " + str(burned_percentage) + "%")
            results[pattern].append(100 - burned_percentage)  # Percentage not burned

    avg_results = {pattern: sum(results[pattern]) / experiments for pattern in patterns}
    return avg_results


avg_results = repeatedExperiments(100, 100, 100, 0.8, 30)
print(avg_results)