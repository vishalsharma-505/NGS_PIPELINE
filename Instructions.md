# 📖 Comprehensive Execution Guide: NGS Pipeline

This pipeline automates RNA-Seq Differential Expression Analysis. It is designed strictly for command-line execution in a Linux environment. Read the following rules carefully before initiating your run. **Failure to follow these rules will result in mid-pipeline crashes, OOM kills, or silent data loss.**

## 🛠️ 1. Environment Setup (First Step)
Before doing anything, you must install all required dependencies. A Conda environment file is provided.

```bash
# Create and activate the environment
conda env create -f environment.yml
conda activate ngs_pipeline
```

## 💻 2. Hardware Requirements & Resource Management (CRITICAL)
This pipeline is resource-intensive. Ensure your system meets these requirements:

*   **RAM & Swap Memory:** A minimum of **16GB physical RAM** is strictly required. Furthermore, it is highly recommended to increase your Linux Swap Memory by at least 8GB to 16GB. The HISAT2 indexing and alignment steps consume massive memory spikes; without enough swap/RAM, the Linux OOM (Out of Memory) killer will terminate the pipeline silently.
*   **Disk Space:** Ensure you have at least 50GB-100GB of free disk space. Intermediate BAM files and indices are large.
*   **Thread Allocation (Avoid CPU Bottlenecks):** 
    *   The pipeline uses piped processes (`hisat2 | samtools view | samtools sort`) to save disk space. This means HISAT2 and Samtools run **simultaneously**. 
    *   **For CPUs WITH Multithreading/Hyperthreading (e.g., 8 cores / 16 threads):** You can safely set the `threads` parameter in `config.yaml` to your physical core count (e.g., `threads: 8`). The 16 available logical threads will easily handle the concurrent processes.
    *   **For CPUs WITHOUT Multithreading (e.g., 8 cores / 8 threads):** Set `threads` to **half** of your total cores (e.g., `threads: 4`). If you set it to 8, HISAT2 and Samtools will fight for the same 8 threads simultaneously, causing severe bottlenecking and potential crashes.

## ⚙️ 3. Configuration (`config.yaml`) Setup
Edit `config/config.yaml` to match your run parameters:

```yaml
project_name : NGS Pipeline
threads : 4  # Read the Thread Allocation rule above!
organism : human
reference :
  fasta : "reference/genome/GRCh38.primary_assembly.genome.fa"
  gtf : "reference/genome/gencode.v50.primary_assembly.annotation.gtf"
  hisat2_index : "reference/index/grch38"
metadata : "config/samples.csv"
strandedness : 0  # 0 = unstranded, 1 = forward stranded, 2 = reverse stranded
```

**Strict Rules:**
*   **Linux Paths Only:** All paths must be valid Linux absolute or relative paths. Windows paths (e.g., `C:\Users\...`) are not supported and will crash the script.
*   **Strandedness:** Do not ignore this. Set it to `0` (unstranded), `1` (forward), or `2` (reverse) based on your library prep kit.

## 🧬 4. Reference Genome & Index Management
*   **Organism Setup:** Place your `.fa` and `.gtf` files inside the `reference/genome/` directory.
*   **The 8-File Index Check:** The script checks for the existence of 8 HISAT2 index files (`.ht2` or `.ht2l`). If missing, it builds them automatically.
*   **Crash Warning:** If you switch organisms (e.g., Human to Mouse), or if an index gets corrupted, you **must manually delete all 8 old index files** in `reference/index/`. The script does not verify the organism species of the existing index files. If you don't delete them, it will align Mouse reads to a Human index.

## 📊 5. Input Data & Metadata Synchronization
Raw FASTQ files and your `samples.csv` metadata must be perfectly synchronized.

### FASTQ Naming Convention
*   Files must strictly end with `_1.fastq.gz` (forward) and `_2.fastq.gz` (reverse).
*   The prefix before `_1.fastq.gz` is read as the **Exact Sample Name**.

### Metadata (`samples.csv`) Structure
*   The CSV must contain exactly two columns: `sample` and `condition`.
*   **Biological Replicates:** DESeq2 requires exactly 2 conditions for pairwise comparison and a minimum of 2 biological replicates per condition.

**Correct Example `samples.csv` (Showing Biological Replicates):**

```csv
sample,condition
WT_Rep1,WildType
WT_Rep2,WildType
WT_Rep3,WildType
KO_Rep1,KnockOut
KO_Rep2,KnockOut
KO_Rep3,KnockOut
```
*(Based on this metadata, your input folder MUST contain `WT_Rep1_1.fastq.gz`, `WT_Rep1_2.fastq.gz`, `WT_Rep2_1.fastq.gz`, etc. Any spelling mismatch between the FASTQ prefix and the `sample` column will crash the DESeq2 step).*

## 🚀 6. Execution
The pipeline isolates results automatically. Every run dynamically creates a new `runs/dataset_X` directory.

Start the pipeline using a strict Linux path:

```bash
# Correct (Linux/WSL Path):
python Pipeline.py --input "/absolute/path/to/fastq/folder"
```

## ⚠️ 7. Additional Edge Cases & Crash Triggers
*   **Corrupt FASTQ Files:** Ensure your `.fastq.gz` files are fully downloaded. A truncated or corrupted gzip file will cause `fastp` or `hisat2` to fail midway.
*   **Reference Naming Mismatch:** The `.fa` and `.gtf` files MUST use identical chromosome naming conventions (e.g., both use `chr1` or both use `1`). Mixing conventions will result in successful alignment but zero assigned counts in `featureCounts`.
