# 1. Download SARS-CoV-2 open data

Downloading data from <https://nextstrain.org/ncov/open/global> and placing into directory `input/`. Data downloaded as of August 12, 2021.

```bash
mkdir input/
cd input/

wget https://data.nextstrain.org/files/ncov/open/sequences.fasta.xz
wget https://data.nextstrain.org/files/ncov/open/metadata.tsv.gz
```

Also downloading preprocessed files to compare everything to in directory `input/nextstrain-preprocessed`. Data downloaded as of August 12, 2021.

```bash
mkdir nextstrain-preprocessed
cd nextstrain-preprocessed

wget https://data.nextstrain.org/files/ncov/open/aligned.fasta.xz
wget https://data.nextstrain.org/files/ncov/open/filtered.fasta.xz
wget https://data.nextstrain.org/files/ncov/open/masked.fasta.xz
wget https://data.nextstrain.org/files/ncov/open/mutation-summary.tsv.xz
```

```bash
find input/ | xargs sha256sum >> sha256.input
```

# 2. Extract sequences to separate files

I currently need every genome to be a separate fasta file to analyze the data in my software. So I need to extract all genomes into separate fasta files.

Run `extract-sequences.ipynb`

# 3. Create index

Run the following:

```bash
gdi init index
gdi --project-dir index --ncores 32 analysis --use-conda --no-load-data --reference-file references/NC_045512.gbk.gz --sample-batch-size 10000 --input-structured-genomes-file input-files.tsv
gdi --project-dir index --ncores 32 load vcf --reference-file references/NC_045512.gbk.gz --sample-batch-size 10000 snakemake-assemblies.1628885062.6623144/gdi-input.fofn
```
