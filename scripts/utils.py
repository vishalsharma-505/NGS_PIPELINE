from pathlib import Path

def get_samples(input_dir) :
 paired_samples = []

 for r1file in input_dir.glob("*_1.fastq.gz"):
    sample_name = r1file.name.replace("_1.fastq.gz","")
    r2file = input_dir / f"{sample_name}_2.fastq.gz" 
    if r2file.exists():
        paired_samples.append(
           [ sample_name, r1file ,r2file]
        )
 return paired_samples