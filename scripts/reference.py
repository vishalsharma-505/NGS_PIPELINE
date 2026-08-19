from pathlib import Path
import subprocess

def prepare_reference(config) :
    fasta = Path(str(config["reference"]["fasta"]))
    index_prefix = Path(str(config["reference"]["hisat2_index"]))  

    ht2_files = []
    for i in range(1,9):
        ht2_files.append(Path(f"{index_prefix}.{i}.ht2"))
    ht2_count = 0

    for file in ht2_files :
        if file.exists() :
            ht2_count +=1
           
    if ht2_count == 8 :
        print("Hisat2 index already exists")
        return
    ht2l_files=[]
    for i in range(1,9) :
        ht2l_files.append(Path(f"{index_prefix}.{i}.ht2l"))


    ht2l_count =0

    for file in ht2l_files :
        if file.exists():
            ht2l_count +=1

    if ht2l_count == 8 :
        print("Hisat2 index already exists")
        return
    

    print("\nBuilding HISAT2 index...")
    index_prefix.parent.mkdir(parents=True,exist_ok=True)  

    command =[
        "hisat2-build",str(fasta),str(index_prefix)
    ]
    subprocess.run(command,check=True)
    print("\nHISAT2 index completed.")

