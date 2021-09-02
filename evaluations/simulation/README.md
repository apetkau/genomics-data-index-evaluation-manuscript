To install, after creating conda environment from `environment.yml` run in R:

```R
install.packages("jackalope", type="source")
install.packages("treespace")
```

Note, please see <https://lucasnell.github.io/jackalope/index.html#enabling-openmp> for enabling openmp to use multiple threads.

Also install <https://github.com/apetkau/genomics-data-index>

# 1. Data simulations

To re-generate all data simulations, please do the following:

```bash
# Clean up any existing data
rm -rf simulations
mkdir simulations

# Run simulations
./1-data-simulation.sh | tee log.1-data-simulation
```

# 2. Indexing genomes


```bash
# Run indexing
./2-index-genomes.sh | tee log.2-index-genomes
```

# 3. Variants comparison

```bash
./3-variants-comparison.sh | tee log.3-variants-comparison
```

# 4. Query

```bash
./4-query-comparison.sh | tee log.4-query-comparison
```
