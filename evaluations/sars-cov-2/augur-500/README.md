# Generate tree with Augur

# 1. Install Augur

```bash
mamba create --name augur augur jupyterlab
conda activate augur

augur --version
# 14.0.0
```

# 2. Prepare input

* Run [1-prepare-input.ipynb][]

## 2.1. Create reference fasta file

```bash
# Uses tool from bioperl
zcat ../references/NC_045512.gbk.gz | bp_seqconvert --from genbank --to fasta > NC_045512.fasta
```

# 3. Generate sequences file

```bash
augur filter --metadata metadata-500.tsv --sequences ../input/all.fasta.gz --output sequences-filtered.fasta --output-metadata metadata-filtered.tsv
```

# 4. Multiple sequence alignment

```bash
augur align --nthreads 48 --sequences sequences-filtered.fasta -o alignment.fasta --reference-sequence NC_045512.fasta
```

# 5. Build tree

```bash
augur tree --nthreads 48 --alignment alignment.fasta -o tree.subs.augur.nwk
```
