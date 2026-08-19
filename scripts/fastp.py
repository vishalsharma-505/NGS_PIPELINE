from pathlib import Path
import subprocess

def run_fastp(samples, threads,run_dir) :  
    output_dir = Path(run_dir/"data/trimmed")
    report_dir = Path(run_dir/"results/fastp")
    output_dir.mkdir(parents=True,exist_ok=True)
    report_dir.mkdir(parents=True,exist_ok=True)
    
    trimmed_samples =[]
    for sample, r1 ,r2 in samples :
        out_r1 = output_dir /f"{sample}_1.trimmed.fastq.gz"   
        out_r2 = output_dir /f"{sample}_2.trimmed.fastq.gz"

        html = report_dir / f"{sample}.html"
        json = report_dir / f"{sample}.json"

        print(f"\nRunning fastp for {sample}")
        
        command = [
            "fastp","-i",str(r1),"-I",str(r2),"-o",str(out_r1),"-O",str(out_r2),  
            "-h",str(html),"-j",str(json),"-w",str(threads)
        ]  

        subprocess.run(command,check= True)

        trimmed_samples.append((sample,out_r1,out_r2))
    print("fastp completed") 
    return trimmed_samples

