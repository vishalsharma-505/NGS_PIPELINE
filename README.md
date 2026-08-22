🧬 Automated RNA-Seq Differential Expression Pipeline
A highly automated, end-to-end command-line workflow for processing RNA-Seq data. This pipeline takes raw paired-end FASTQ files and generates read alignments, gene counts, and publication-ready differential expression visualizations with zero manual intervention.

⚠️ CRITICAL WARNING:
This pipeline is highly resource-intensive. Execution time varies significantly based on your hardware, total sample count, and sequencing depth. To avoid mid-run crashes, OOM (Out of Memory) kills, or silent data loss, you MUST read the full Execution Guide (instructions.md) before setting up your data and config.

⚡ Pipeline Workflow
Quality Control & Trimming: Raw read assessment with FastQC, adapter/quality trimming via fastp, and aggregated reporting using MultiQC.

Alignment: Reference genome indexing and read mapping using HISAT2, with automated BAM sorting and indexing via Samtools.

Quantification: Gene-level read counting using featureCounts.

Differential Expression & Visualization: Statistical analysis using PyDESeq2, automatically generating PCA plots, Volcano plots, MA plots, and expression heatmaps.

💻 Quick Requirements
OS: Native Linux or Windows Subsystem for Linux (WSL). Strict absolute Linux paths only.

Hardware: Minimum 16GB RAM is required for HISAT2 human genome indexing and alignment. Additional Linux Swap memory is highly recommended. CPU threads should be scaled according to your system capacity.

Environment: All dependencies are managed via Conda (environment.yml).

🚀 Quick Start
Clone this repository to your local machine.

Create and activate the conda environment:

Bash
conda env create -f environment.yml
conda activate ngs_pipeline
Update config/config.yaml and config/samples.csv according to the Execution Guide.

Run the pipeline:

Bash
python Pipeline.py --input /absolute/linux/path/to/fastq_folder
(Note: Output files, logs, and plots are safely isolated and dynamically saved in automatically generated runs/dataset_X/ directories.)
