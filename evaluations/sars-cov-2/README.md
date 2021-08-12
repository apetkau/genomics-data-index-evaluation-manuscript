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
