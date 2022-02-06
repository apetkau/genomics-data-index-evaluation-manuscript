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

## 1.4. Fix and cosolidate all reads

Some read-pairs differ in their names in that they have `_forward` and `_reverse` in the identifiers, which causes issues when running snippy. I need to strip all these out. This is done with the following notebook:

* `1-fix-reads.ipynb`

This outputs all gzipped fastq files to a directory `data/fastq`.

# 1.5. Reference genomes

Each of these was downloaded by looking at the `datasets/datasets/*.tsv` file for the reference genome in the column **suggestedReference**. I searched for these on NCBI. Some of the reference genomes have been updated since the tsv files were written. I downloaded the latest version by looking for the **FTP directory for RefSeq assembly** link on NCBI and downloading the `.gbff.gz` file.

```bash
mkdir reference
cd reference

mkdir campylobacter
pushd campylobacter
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/879/185/GCA_001879185.2_ASM187918v2/GCA_001879185.2_ASM187918v2_genomic.gbff.gz
mv GCA_001879185.2_ASM187918v2_genomic.gbff.gz GCA_001879185.2_ASM187918v2_genomic.gbk.gz
popd

mkdir listeria
pushd listeria
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/001/047/715/GCF_001047715.2_ASM104771v2/GCF_001047715.2_ASM104771v2_genomic.gbff.gz
mv GCF_001047715.2_ASM104771v2_genomic.gbff.gz GCF_001047715.2_ASM104771v2_genomic.gbk.gz
popd

mkdir ecoli
pushd ecoli
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/703/365/GCF_000703365.1_Ec2011C-3609/GCF_000703365.1_Ec2011C-3609_genomic.gbff.gz
mv GCF_000703365.1_Ec2011C-3609_genomic.gbff.gz GCF_000703365.1_Ec2011C-3609_genomic.gbk.gz
popd

mkdir salmonella
pushd salmonella
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/439/415/GCF_000439415.1_ASM43941v1/GCF_000439415.1_ASM43941v1_genomic.gbff.gz
mv GCF_000439415.1_ASM43941v1_genomic.gbff.gz GCF_000439415.1_ASM43941v1_genomic.gbk.gz
popd
```

## 1.6. Create metadata table

Next, I create a combined metadata table with all samples using:

* `2-create-input-list.ipynb`

# 2. Analysis

To perform the analysis of all genomes I run the following:

```bash
mamba env create  --name gdi-reads --file environment.yml
conda activate gdi-reads

papermill template-3-index-genomes.ipynb 3-index-genomes.ipynb
```

