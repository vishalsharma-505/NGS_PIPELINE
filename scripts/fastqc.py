import subprocess
from pathlib import Path                    

def run_fastqc(samples, threads,output_path) :
 output_dir = Path(output_path)
 output_dir.mkdir(parents=True, exist_ok=True) 

 for sample ,r1 ,r2 in samples :
  print(f"running fastqc for sample {sample}")

  command = ["fastqc","-t",str(threads),"-o",str(output_dir),str(r1),str(r2)]

  subprocess.run(command,check=True) 
  