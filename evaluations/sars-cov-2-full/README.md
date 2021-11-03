Create a full index of all SARS-CoV-2 open data.

# 1. Download SARS-CoV-2 open data

Downloading data from <https://nextstrain.org/ncov/open/global> and placing into directory `input/`. Data downloaded as of November 11, 2021.

```bash
mkdir input/
cd input/

wget https://data.nextstrain.org/files/ncov/open/sequences.fasta.xz
wget https://data.nextstrain.org/files/ncov/open/metadata.tsv.gz
```

# 2. Extract sequences to separate files

```bash
gdi input-split-file --output-dir fasta --output-samples-file input.tsv --absolute sequences.fasta.xz
```

# 3. Create index

Run the following:

```bash
gdi init index
gdi --project-dir index --ncores 32 analysis --use-conda --no-load-data --reference-file references/NC_045512.gbk.gz --sample-batch-size 10000 --input-structured-genomes-file input-files.tsv
gdi --project-dir index --ncores 32 load vcf --reference-file references/NC_045512.gbk.gz --sample-batch-size 10000 snakemake-assemblies.1628885062.6623144/gdi-input.fofn
```
