# Forest Fire Thinning Strategies - A Cellular Automaton Model

## Overview

This project investigates the effects of different forest thinning strategies on the spread of wildfires using a cellular automaton model. Given the increasing threat of forest fires due to climate change, understanding how thinning techniques influence fire spread is crucial for developing effective mitigation strategies.

Forest thinning is a method used to reduce the density of trees in a forest, which can help slow down or stop the spread of fires. However, the impact of different spatial thinning patterns on fire spread is not well understood. 

This project uses a modified version of the Mesa forest fire model to simulate and analyze the effects of three distinct thinning patterns: random distribution, clustered distribution, and striped distribution.

More information is found in `Project_Report.pdf`.

## Model

The project utilizes a modified version of the Mesa forest fire model, which simulates fire spreading through a grid of cells representing trees. 

The model incorporates three key modifications:

#### Probability Adjustment:
The probability of neighboring cells catching fire has been reduced from 100% to 80%, to reflect that not all trees are equally flammable.

#### Fire Jumping: 
A 5% probability is introduced for the fire to "jump" to cells within a 16-cell radius, simulating wind-driven fire spread.

#### Spatial Distribution: 
The model supports three spatial patterns for tree distribution:
- Random Distribution: Trees are placed randomly across the grid.
- Clustered Distribution: Trees are grouped into random clusters, simulating areas of cleared land.
- Striped Distribution: Trees are arranged in long, narrow strips, creating firebreaks.

## Running the Model

To run the model, follow these steps:

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Run One Iteration of the Simulation

```bash
python model/run.py
```

#### Perform a Batch Run of the Simulation

```bash
python model/batchrunner.py
```

Results will be saved in the results.csv.

## Simulation Parameters 

The model is run for three different tree densities: 50%, 65%, and 80%. 

Each thinning pattern is simulated 100 times for each density to obtain average results. 

Key metrics include the percentage of area burned and the time taken for the fire to stop spreading.

## Results 

- Random and Clustered Distributions: Both patterns show a high burn rate, with approximately 93-96% of the area consumed by fire. These patterns leave small clusters of unburned trees, but most of the forest is destroyed.

- Striped Distribution: This pattern significantly reduces the spread of fire, with only about 30-55% of the area burned, depending on the density. The striped pattern acts as an effective firebreak, containing the fire earlier and leaving large portions of the forest unscathed.

- Density Impact: Higher densities result in faster fire spread and greater overall destruction. The striped pattern consistently performs better than the other two patterns across all densities.
