Install conda environment from `environment.yml`. Also install <https://github.com/apetkau/genomics-data-index>.

# 1. Get data

To get data please do the following:

## 1.1. Install environment

```bash
mamba env create  --name gdi-reads-datasets --file environment-datasets.yml
conda activate gdi-reads-datasets
```

## 1.2. Clone repo and install other dependencies

```bash
cd data/
git clone https://github.com/WGS-standards-and-analysis/datasets.git
cd datasets

# Following instructions in README.md from cloned repository
export PATH=$PWD/scripts:$PATH

## Install edirect
# Follow instructions in repository github
# I found there was no ./edirect/setup.sh which exists so I skipped this step
export PATH=$HOME/bin/edirect:$PATH
```

### 1.2.1. Install missing dependencies

The following are missing from the original instructions

```bash
pushd ~/bin
nquire -dwn ftp.ncbi.nlm.nih.gov entrez/entrezdirect xtract.Linux.gz
gunzip -f xtract.Linux.gz
chmod +x xtract.Linux
ln -s xtract.Linux xtract

nquire -dwn ftp.ncbi.nlm.nih.gov entrez/entrezdirect transmute.Linux.gz
gunzip -f transmute.Linux.gz
chmod +x transmute.Linux
ln -s transmute.Linux transmute

export PATH=$HOME/bin:$PATH
popd
```

## 1.3. Download datasets

Running `GenFSGopher.pl` to download datasets.

```bash
GenFSGopher.pl --outdir Campylobacter_jejuni_0810PADBR-1 --layout byformat --numcpus 4 datasets/Campylobacter_jejuni_0810PADBR-1.tsv
# This errored out and I had to go into the Campylobacter_jejuni_0810PADBR-1/ directory and run
# make -j 4

GenFSGopher.pl --outdir Salmonella_enterica_1203NYJAP-1 --layout byformat --numcpus 4 datasets/Salmonella_enterica_1203NYJAP-1.tsv
# This errored out and I had to go into Salmonella_enterica_1203NYJAP-1/ and run
# make -j 4
# All the genbank file checksums failed but the reads succeeded
```

Repeat the same for `datasets/Escherichia_coli_1405WAEXK-1.tsv` and `datasets/Listeria_monocytogenes_1408MLGX6-3WGS.tsv`.
