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
from genomics_data_index.storage.io.mutation.SequenceFile import SequenceFile


class IndexBenchmarker:
    
    def __init__(self, index_path: Path, input_files_file: Path, reference_file: Path, ncores: int, mincov: int = 5):
        self._ncores = ncores
        self._mincov = mincov
        self._index_path = index_path
        self._input_files_file = input_files_file
        self._reference_file = reference_file
        self._reference_name, records = SequenceFile(reference_file).parse_sequence_file()
        
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

    def benchmark(iterations: int = 1):
        pass


    def build_index_analysis(self, iteration: int, build_tree: bool = False):
        print(f'\nIteration {iteration} of index/analysis of {self._number_samples} samples with {self._ncores} cores')

        snakemake_dirs = glob.glob('snakemake*')
        print(f'Removing any extra snakemake directories: {snakemake_dirs}')
        for d in snakemake_dirs:
            rmtree(d)

        if self._index_path.exists():
            print(f'Removing any existing indexes {self._index_path}')
            rmtree(self._index_path)

        create_index_cmd = f'gdi init {self._index_path}'
        print(f'Creating new index: [{create_index_cmd}]')
        before_time = time.time()
        cmdbench.benchmark_command(create_index_cmd, iterations_num=1)
        after_time = time.time()
        print(f'Creating a new index took {(after_time - before_time):0.2f} seconds')

        analysis_cmd = (
            f"gdi --project-dir {self._index_path} --ncores {self._ncores} analysis"
            f" --use-conda --no-load-data --reference-file {self._reference_file}" 
            f" --reads-mincov {self._mincov}"
            f" --input-structured-genomes-file {self._input_files_file}"
        )
        print(f"Analysis running: [{analysis_cmd}]")
        before_time = time.time()
        benchmark_analysis = cmdbench.benchmark_command(analysis_cmd, iterations_num=1)
        after_time = time.time()
        print(f'Analysis took {(after_time - before_time)/60:0.2f} minutes')

        index_input_file = self._get_and_validate_index_input(expected_number_samples=self._number_samples)
        index_cmd = (
            f"gdi --project-dir {self._index_path} --ncores {self._ncores} load vcf"
            f" --reference-file {self._reference_file} {index_input_file}"
        )
        print(f"Index running: [{index_cmd}]")
        before_time = time.time()
        benchmark_index = cmdbench.benchmark_command(index_cmd, iterations_num = 1)
        after_time = time.time()
        print(f'Indexing took {(after_time - before_time)/60:0.2f} minutes')

        if build_tree:
            build_cmd = (
                f"gdi --project-dir {self._index_path} --ncores {self._ncores} rebuild tree"
                f" --align-type full --extra-params '--fast -m GTR+F+R4' --reference-name {self._reference_name}"
            )
            print(f"Building tree: [{build_cmd}]")
            before_time = time.time()
            benchmark_tree = cmdbench.benchmark_command(build_cmd, iterations_num = 1)
            after_time = time.time()
            print(f'Building tree took {(after_time - before_time)/60:0.2f} minutes')
        else:
            benchmark_tree = None

        return {
            'analysis': benchmark_analysis,
            'index': benchmark_index,
            'tree': benchmark_tree
        }

