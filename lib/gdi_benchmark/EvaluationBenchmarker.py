import glob
from pathlib import Path
import pandas as pd
import cmdbench
import time
from shutil import rmtree
import gzip
from Bio import SeqIO
from typing import List, Dict, Callable, Any
import subprocess
import genomics_data_index.api as gdi
from genomics_data_index.storage.io.mutation.SequenceFile import SequenceFile
import timeit


class QueryBenchmarkHandler:

    def __init__(self):
        pass

    def _benchmark_to_df(self, name: str, kind: str, iteration: int, number_samples: int, number_features_no_unknown: int, number_features_all: int,
            benchmark_query) -> pd.DataFrame:
        benchmark_query_results = benchmark_query.get_first_iteration()

        df = pd.DataFrame(data={
            'Name': [name],
            'Kind': [kind],
            'Iteration': [iteration],
            'Number samples': [int(number_samples)],
            'Number features (no unknown)': [int(number_features_no_unknown)],
            'Number features (all)': [int(number_features_all)],
            'Runtime': [float(benchmark_query_results['process']['execution_time'])],
            'Memory (max)': [float(benchmark_query_results['memory']['max'])],
            'Mmemory (max/process)': [float(benchmark_query_results['memory']['max_perprocess'])],
        })

        return df

    def benchmark_cli(self, name: str, kind_commands: Dict[str, str], number_samples: int, number_features_no_unknown: int, number_features_all: int, 
            iterations: int) -> pd.DataFrame:
        results = []
        for kind in kind_commands:
            command = kind_commands[kind]
            for iteration in range(iterations):
                benchmark_query = cmdbench.benchmark_command(command, iterations_num = 1)
                kind_iteration_df = self._benchmark_to_df(name=name, kind=kind, iteration=iteration+1, number_samples=number_samples,
                                                          number_features_no_unknown=number_features_no_unknown,
                                                          number_features_all=number_features_all, benchmark_query=benchmark_query)
                results.append(kind_iteration_df)
        return pd.concat(results)

    
    def benchmark_api(self, name: str, kind_functions: Dict[str, Callable[[Any], Any]], number_samples: int, 
            number_features_no_unknown: int, number_features_all: int, repeat: int) -> pd.DataFrame:
        results = []
        for kind in kind_functions:
            func = kind_functions[kind]
            timer = timeit.Timer(func)
            number_loops = timer.autorange()[0]
            result = timer.repeat(repeat=repeat, number=number_loops)
            result = list(map(lambda x: x/number_loops, result)) # Convert to time per single execution
            df = self._create_timing_df_single_case(result, name=name, kind=kind, number_samples=number_samples,
                    number_features_no_unknown=number_features_no_unknown, number_features_all=number_features_all, number_loops=number_loops)
            results.append(df)

        return pd.concat(results)


    def _create_timing_df_single_case(self, timings: List[float], name: str, kind: str,
                                      number_samples: int, number_features_no_unknown: int,
                                      number_features_all: int, number_loops: int) -> pd.DataFrame:
        iterations = len(timings)
        return pd.DataFrame({
            'Name': [name]*iterations,
            'Kind': [kind]*iterations,
            'Number samples': [number_samples]*iterations,
            'Number features (no unknown)': [number_features_no_unknown]*iterations,
            'Number features (all)': [number_features_all]*iterations,
            'Number executions': number_loops,
            'Iteration': range(1, iterations + 1),
            'Time': timings,
        })


class BenchmarkResultsHandler:
    
    def __init__(self, name: str):
        self._name = name
    
    def benchmark_to_df(self, iteration: int, number_samples: int, benchmark_analysis, benchmark_index, benchmark_tree,
                    index_path: Path, analysis_path: Path,
                    ncores: int, reference_length: int) -> pd.DataFrame:
        analysis_data = benchmark_analysis.get_first_iteration()
        index_data = benchmark_index.get_first_iteration()
        tree_data = benchmark_tree.get_first_iteration() if benchmark_tree is not None else None

        analysis_size = subprocess.check_output(
            ['du', '-s', '--block-size=1', str(analysis_path)]).split()[0].decode('utf-8')

        db = gdi.GenomicsDataIndex.connect(index_path)
        index_size = db.db_size(unit='B').set_index('Type').loc['Total']['Data Size (B)']

        tree_runtime = float(tree_data['process']['execution_time']) if tree_data is not None else pd.NA
        tree_memory_max = float(tree_data['memory']['max']) if tree_data is not None else pd.NA
        tree_memory_max_proc = float(tree_data['memory']['max_perprocess']) if tree_data is not None else pd.NA

        df = pd.DataFrame(data={
            'Name': [self._name],
            'Iteration': [iteration],
            'Number samples': [int(number_samples)],
            'Number cores': [ncores],
            'Reference length': [reference_length],
            'Analysis runtime': [float(analysis_data['process']['execution_time'])],
            'Analysis memory (max)': [float(analysis_data['memory']['max'])],
            'Analysis memory (max/process)': [float(analysis_data['memory']['max_perprocess'])],
            'Analysis disk uage': [float(analysis_size)],
            'Index runtime': [float(index_data['process']['execution_time'])],
            'Index memory (max)': [float(index_data['memory']['max'])],
            'Index memory (max/process)': [float(index_data['memory']['max_perprocess'])],
            'Index size': [index_size],
            'Tree runtime': [tree_runtime],
            'Tree memory (max)': [tree_memory_max],
            'Tree memory (max/process)': [tree_memory_max_proc],
        })

        if not pd.isna(tree_runtime):
            df['Total runtime'] = df['Analysis runtime'] + df['Index runtime'] + df['Tree runtime']
        else:
            df['Total runtime'] = df['Analysis runtime'] + df['Index runtime']

        if not pd.isna(tree_memory_max):
            df['Max memory'] = df[['Analysis memory (max)', 'Index memory (max)', 'Tree memory (max)']].max(axis='columns')
        else:
            df['Max memory'] = df[['Analysis memory (max)', 'Index memory (max)']].max(axis='columns')

        return df

    def convert_sizes(self, df: pd.DataFrame) -> pd.DataFrame:
        size_factor = 1024**3 # GB
        time_factor = 60 # min

        new_df = df.copy()
        size_cols = ['Analysis memory (max)', 'Analysis memory (max/process)',
               'Analysis disk uage', 'Index memory (max)', 'Index memory (max/process)',
               'Index size', 'Max memory']
        time_cols = ['Analysis runtime', 'Index runtime', 'Total runtime']

        for col in size_cols:
            new_df[col] = df[col] / size_factor

        for col in time_cols:
            new_df[col] = df[col] / time_factor

        return new_df


class IndexBenchmarker:
    
    def __init__(self, benchmark_results_handler: BenchmarkResultsHandler,
                       index_path: Path, input_files_file: Path, reference_file: Path, ncores: int, mincov: int = 5, build_tree: bool = False):
        self._ncores = ncores
        self._mincov = mincov
        self._index_path = index_path
        self._input_files_file = input_files_file
        self._reference_file = reference_file
        self._reference_name, records = SequenceFile(reference_file).parse_sequence_file()
        self._reference_length = 0
        for record in records:
            self._reference_length = self._reference_length + len(record)
        self._build_tree = build_tree
        self._benchmark_results_handler = benchmark_results_handler
        
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

    def benchmark(self, iterations: int = 1) -> pd.DataFrame:
        index_df_iterations = []
        for iteration in range(1, iterations + 1):
           index_df_iterations.append(self.build_index_analysis(iteration))

        return pd.concat(index_df_iterations)

    def build_index_analysis(self, iteration: int) -> pd.DataFrame:
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
            f" --kmer-size 31 --kmer-size 51 --kmer-size 71 --include-kmer"
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
            f"gdi --project-dir {self._index_path} --ncores {self._ncores} load vcf-kmer"
            f" --reference-file {self._reference_file} {index_input_file}"
        )
        print(f"Index running: [{index_cmd}]")
        before_time = time.time()
        benchmark_index = cmdbench.benchmark_command(index_cmd, iterations_num = 1)
        after_time = time.time()
        print(f'Indexing took {(after_time - before_time)/60:0.2f} minutes')

        if self._build_tree:
            build_cmd = (
                f"gdi --project-dir {self._index_path} --ncores {self._ncores} rebuild tree"
                f" --align-type full --extra-params '--fast -m GTR+F+R4' {self._reference_name}"
            )
            print(f"Building tree: [{build_cmd}]")
            before_time = time.time()
            benchmark_tree = cmdbench.benchmark_command(build_cmd, iterations_num = 1)
            after_time = time.time()
            print(f'Building tree took {(after_time - before_time)/60:0.2f} minutes')
        else:
            benchmark_tree = None

        benchmark_df = self._benchmark_results_handler.benchmark_to_df(iteration=iteration,
                                                       number_samples=self._number_samples,
                                                       benchmark_analysis=benchmark_analysis,
                                                       benchmark_index=benchmark_index,
                                                       benchmark_tree=benchmark_tree,
                                                       index_path=self._index_path,
                                                       analysis_path=index_input_file.parent,
                                                       ncores=self._ncores,
                                                       reference_length=self._reference_length)
         
        return benchmark_df
