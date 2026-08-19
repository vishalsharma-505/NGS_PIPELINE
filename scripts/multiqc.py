from pathlib import Path
import subprocess

def run_multiqc(run_dir) :
    output_dir = Path(run_dir/"results/multiqc")
    output_dir.mkdir(parents=True,exist_ok=True)

    command = [
        "multiqc", str(run_dir/"results/fastqc_raw"), str(run_dir/"results/fastqc_trimmed"), str(run_dir/"results/fastp"),"-o",str(output_dir)
    ]
    print("\nRunning MultiQC")
    subprocess.run(command,check=True)
    print("\nMultiQC Completed")
