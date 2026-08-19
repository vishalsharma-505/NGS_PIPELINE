from pathlib import Path
import subprocess

def hisat_alignment(trimmed_samples,config,run_dir) :
  index_prefix = config["reference"]["hisat2_index"]
  bam_dir = Path(run_dir/"results/alignment/bam")
  stats_dir = Path(run_dir/"results/alignment/stats")
  log_dir = Path(run_dir/"logs/hisat2")

  bam_dir.mkdir(parents=True,exist_ok=True)
  log_dir.mkdir(parents=True,exist_ok=True)
  stats_dir.mkdir(parents=True,exist_ok=True)

  for sample, r1, r2 in trimmed_samples :
    log_file = log_dir / f"{sample}.hisat2_samtools.log"
    bam_file = bam_dir/ f"{sample}.sorted.bam"
    flagstat_file = stats_dir/ f"{sample}.flagstat.txt"


    hisat_align = [ "hisat2",
              "-x", index_prefix,  
            "-1", str(r1),
            "-2", str(r2),
            "-p", str(config["threads"]) ]
    
    samtools_sam_to_bam = [
      "samtools","view","-b","-"
    ]
    samtools_sort_bam = [
      "samtools","sort","-@",str(config["threads"]),"-o",str(bam_file),"-"
    ]

    samtools_index_bam = [
      "samtools","index",str(bam_file)
    ]
    samtools_flagstat = [
      "samtools","flagstat",str(bam_file)
    ]

    with open (log_file,"w") as log :

      process1 = subprocess.Popen(
        hisat_align,
        stdout= subprocess.PIPE,
        stderr= log
      )
      process2 = subprocess.Popen(
        samtools_sam_to_bam,
        stdin=process1.stdout,
        stdout= subprocess.PIPE,
        stderr= log
        )
      process3 = subprocess.Popen(
        samtools_sort_bam,
        stdin= process2.stdout,
        stderr= log
        
      )
      process1.stdout.close() 
      process2.stdout.close()

      process3.communicate()

      process1.wait()
      process2.wait()
      



      if process1.returncode != 0:
       raise RuntimeError(f"HISAT2 failed for {sample}")

      if process2.returncode != 0:
        raise RuntimeError(f"samtools view failed for {sample}")
      if process3.returncode != 0 :
        raise RuntimeError(f"samtools sort failed for {sample}")
      
    subprocess.run(samtools_index_bam,check=True)

    with open(flagstat_file,"w") as stats :
      subprocess.run(samtools_flagstat,check=True,stdout=stats)

    print(f"finished {sample}")

  print("\nAlignment completed")

   


