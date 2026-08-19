from pathlib import Path
import subprocess

def feature_counts(config,run_dir) :
    bam_dir = Path(run_dir/"results/alignment/bam")
    count_dir = Path(run_dir/"results/counts")
    count_dir.mkdir(parents=True,exist_ok=True)

    bam_files = sorted(bam_dir.glob("*sorted.bam"))
     
    if not bam_files :
        raise FileNotFoundError("No BAM files found")
    
    output_file = count_dir/ 'gene_counts.txt'
    
    command =[
        "featureCounts" ,
        "-T", str(config["threads"]),
        "-p",
        "-a", str(config["reference"]["gtf"]),
        "-o", str(output_file)
    ]

    for bam in bam_files :
        command.append(str(bam))
    
    subprocess.run(command,check=True)

    print("\nfeatureCounts Completed")
    
