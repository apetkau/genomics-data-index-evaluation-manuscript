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

class BenchmarkResultsHandler:
    
    def __init__(self):
        pass
    
    def benchmark_to_df(self, iteration: int, number_samples: int, benchmark_analysis, benchmark_index,
                    index_path: Path, analysis_path: Path,
                    ncores: int, reference_length: int) -> pd.DataFrame:
        analysis_data = benchmark_analysis.get_first_iteration()
        index_data = benchmark_index.get_first_iteration()

        analysis_size = subprocess.check_output(
            ['du', '-s', '--block-size=1', str(analysis_path)]).split()[0].decode('utf-8')

        db = gdi.GenomicsDataIndex.connect(index_path)
        index_size = db.db_size(unit='B').set_index('Type').loc['Total']['Data Size (B)']

        df = pd.DataFrame(data={
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
        })

        df['Total runtime'] = df['Analysis runtime'] + df['Index runtime']
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

