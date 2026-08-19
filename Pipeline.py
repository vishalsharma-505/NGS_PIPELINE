from scripts.utils import get_samples 
from scripts.fastqc import run_fastqc
from scripts.fastp import run_fastp
from scripts.multiqc import run_multiqc
from scripts.reference import prepare_reference
from scripts.hisat import hisat_alignment
from scripts.featurecounts import feature_counts
from scripts.deseq import run_deseq2
from scripts.gene_filter import filter_significant_genes
from scripts.validate_input import validate_input
from scripts.pca_plot import plot_pca
from scripts.sample_cor_heatmap import plot_sample_correlation
from scripts.ma_plot import plot_ma
from scripts.volcano_plot import plot_volcano
from scripts.expression_heatmap import plot_expression_heatmap

import yaml
import argparse
from pathlib import Path


print("RNA-seq pipeline started")

parser = argparse.ArgumentParser() 
parser.add_argument("--input",required=True,help="Path to folde containing raw FASTQ files")
arg = parser.parse_args()

input_dir = Path(arg.input)

if not input_dir.is_dir():
    raise FileNotFoundError(
        f"Input directory is invalid: {input_dir}"
    )

with open("config/config.yaml") as file :
 config = yaml.safe_load(file)

validate_input(config)
samples = get_samples(input_dir)

if not samples :
 raise ValueError( "No valid paired FASTQ samples found in input directory")

print(f"detected {len(samples)} samples")

runs = Path("runs")
runs.mkdir(exist_ok=True)

dataset_number =1

while (runs/ f"dataset_{dataset_number}").exists() :
 dataset_number +=1
 
run_dir = Path(runs/f"dataset_{dataset_number}")
run_dir.mkdir()
 

run_fastqc(samples,config["threads"],run_dir/"results/fastqc_raw")

trimmed_samples = run_fastp(samples,config['threads'],run_dir)

run_fastqc(trimmed_samples,config["threads"],run_dir/"results/fastqc_trimmed")

run_multiqc(run_dir)
prepare_reference(config)
hisat_alignment(trimmed_samples,config,run_dir)
feature_counts(config,run_dir)


dds, results = run_deseq2(config,run_dir)

filter_significant_genes(run_dir)
plot_pca(dds,run_dir)
plot_sample_correlation(dds,run_dir)
plot_ma(results,run_dir)
plot_volcano(results,run_dir)
plot_expression_heatmap(dds,run_dir)






