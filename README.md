# Genomics data index evaluations

This repository consists of a series of evaluations (as Bash, Python, and Jupyter notebooks) for the [Genomics Data Index][]. These comparisons include run time/memory results that were measured using [cmdbench][].

The evaluations are divided up into three different categories:

1. **[Data simulation](evaluations/simulation)**: An evaluation by simulating a reference genome, mutations, and sequence reads.
   1. [Figures: Trees](evaluations/simulation/6-compare-trees.ipynb): The Jupyter notebook comparing the produced phylogenetic trees.
   2. [Figures: Other](evaluations/simulation/7-comparing-results.ipynb): The Jupyter notebook containing other figures.
2. **[SARS-CoV-2 genome assemblies](evaluations/sars-cov-2)**: An evaluation by loading a subset of SARS-CoV-2 genomes.
   1. [Figures](evaluations/sars-cov-2/5-compare-results.ipynb): The Jupyter notebook containing the figures.
3. **[Bacterial WGS reads](evaluations/reads)**: An evaluation by loading a set of WGS sequence reads derived from a number of bacterial species.
   1. [Figures](evaluations/reads/6-compare-results.ipynb): The Jupyter notebook containing the figures.

[Genomics Data Index]: https://github.com/apetkau/genomics-data-index
[cmdbench]: https://github.com/manzik/cmdbench
