#! /usr/bin/env python
from ruffus import *

import staphopia.tasks.fastq as fastq

parser = cmdline.get_argparse(description='WHAT DOES THIS PIPELINE DO?')
parser.add_argument("--input_file")
options = parser.parse_args()

config = {
    'fastq_cleanup':'/home/rpetit/staphopia/analysis-pipeline/bin/fastq_cleanup',
    'fastq_stats':'/home/rpetit/staphopia/analysis-pipeline/bin/fastq_stats',
    'fastq_validator':'/home/rpetit/staphopia/analysis-pipeline/bin/fastq_validator',
}

# Pipeline --------------------------------------------------------------------
def validator():
    results = fastq.validator(options.input_file, config)

@transform(options.input_file, suffix('.gz'), '.stats')
def raw_stats(input_file, output_file):
    results = fastq.stats(input_file, output_file, config)

@transform([options.input_file], regex(r"(.*).fastq.gz"), 
           r"\1.cleanup.fastq.gz", r"\1.fastq.stats")
def cleanup(input_file, output_file, stats_file):
    results = fastq.cleanup(input_file, stats_file, output_file, config)

@transform(cleanup, suffix('.gz'), '.stats')
def cleanup_stats(input_file, output_file):
    results = fastq.stats(input_file, output_file, config)

# -----------------------------------------------------------------------------
pipeline_run(exceptions_terminate_immediately = True, verbose=5)