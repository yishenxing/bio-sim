# Population Gender Structure Simulation

This Python script simulates how naive fertility choices affect a population's gender structure.

## Key Features

- Simulates `N` families with varying boy-preference intensities
- Models two reproduction strategies:
  - **Boy-preferring families**: Continue having children until a boy is born
  - **Neutral families**: Have children without gender preference
- Generates gender ratio statistics and visualizations

## Parameters

| Parameter | Description |
|-----------|-------------|
| `num_family` | Total number of families to simulate |
| `ratio_boy_family` | Proportion of families with boy preference (0.0-1.0) |
| `num_sim` | Number of simulation iterations |

## Outputs

1. **Text file** (`boy_born_sim.txt`):
   - Average male/female ratio across simulations
   
2. **Visualizations** (PNG files):
   - Histograms of gender ratio distributions for each parameter set

## Dependencies

- `matplotlib` 

## Usage

```bash
python boy_born.py
```

## Conclustion

**This preference will not affect the overall gender ratio in a large population.**



