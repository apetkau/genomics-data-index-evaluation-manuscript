import glob
from pathlib import Path
import pandas as pd
import cmdbench
import time
from shutil import rmtree
import gzip
from Bio import SeqIO
from typing import List
import pandas as pd
import time
import cmdbench
import glob
from shutil import rmtree
import subprocess
import genomics_data_index.api as gdi


class IndexBenchmarker:
    
    def __init__(self, index_path: Path, input_files_file: Path, reference_file: Path, ncores: int, mincov: int = 5):
        self._ncores = ncores
        self._mincov = mincov
        self._index_path = index_path
        self._input_files_file = input_files_file
        self._reference_file = reference_file
        
        input_df = pd.read_csv(input_files_file, sep='\t')
        self._number_samples = len(input_df)

    def _get_and_validate_index_input(self, expected_number_samples):
        snakemake_dirs = glob.glob('snakemake*')
        if len(snakemake_dirs) == 1:
            snakemake_dir = snakemake_dirs[0]
        else:
            raise Exception(f'Invalid number of snakemake directories: {snakemake_dirs}')

        vcf_input_file = (Path(snakemake_dir) / 'gdi-input.fofn').absolute()

        if not vcf_input_file.exists():
            raise Exception(f'VCF input file {vcf_input_file} does not exist')

        vcf_df = pd.read_csv(vcf_input_file, sep='\t')
        actual_number_samples = len(vcf_df)

        assert expected_number_samples == actual_number_samples, f'expected={expected_number_samples} != actual={actual_number_samples}'

        return vcf_input_file

    def build_index_analysis(self, iteration: int):
        snakemake_dirs = glob.glob('snakemake*')
        print(f'Removing any extra snakemake directories: {snakemake_dirs}')
        for d in snakemake_dirs:
            rmtree(d)

        print(f'\n***ANALYSIS of {self._number_samples} samples with {self._ncores} cores')
        analysis_cmd = (
            f"gdi --project-dir {self._index_path} --ncores {self._ncores} analysis"
            f" --use-conda --no-load-data --reference-file {self._reference_file}" 
            f" --reads-mincov {self._mincov}"
            f" --input-structured-genomes-file {self._input_files_file}"
        )
        print(f"Iteration {iteration}: running: [{analysis_cmd}]")
        before_time = time.time()
        benchmark_analysis = cmdbench.benchmark_command(analysis_cmd)
        after_time = time.time()
        print(f'Analysis took {(after_time - before_time)/60:0.2f} minutes')

        print(f'\n***INDEX of {self._number_samples} samples with {self._ncores} cores***')
        index_input_file = self._get_and_validate_index_input(expected_number_samples=self._number_samples)
        index_cmd = (
            f"gdi --project-dir {self._index_path} --ncores {self._ncores} load vcf"
            f" --reference-file {self._reference_file} {index_input_file}"
        )
        print(f"Running: [{index_cmd}]")
        before_time = time.time()
        benchmark_index = cmdbench.benchmark_command(index_cmd, iterations_num = 1)
        after_time = time.time()
        print(f'Indexing took {(after_time - before_time)/60:0.2f} minutes')

        return benchmark_index

