To install, after creating conda environment from `environment.yml` run in R:

```R
install.packages("jackalope", type="source")
```

Note, please see <https://lucasnell.github.io/jackalope/index.html#enabling-openmp> for enabling openmp to use multiple threads.

# 1. Data simulations

To re-generate all data simulations, please do the following:

```bash
# Clean up any existing data
rm -rf simulations
mkdir simulations

# Run simulations
./1-data-simulation.sh | tee log.1-data-simulation
```
