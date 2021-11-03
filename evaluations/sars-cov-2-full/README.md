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

# 4. Split input file into chunks

```bash
cd input
mkdir input-split
cd input-split

# Split file into pieces of size 2000 but keep header
# From https://stackoverflow.com/a/53062251
cat ../input.tsv | parallel --header : --pipe -N2000 'cat >{#}_input-split.tsv'


# Add leading 0s to numbers in file names so it's easier to sort in numerical order
prename 's/^(\d)_/00\1_/' *.tsv
prename 's/^(\d\d)_/0\1_/' *.tsv
prename 's/^(\d\d\d)_/0\1_/' *.tsv
```

# 4. Create index

Run the following:

```bash
gdi init index
```

# 5. Load data into index

```bash
./scripts/index-data.sh 2>&1 | tee index-data.log
```
