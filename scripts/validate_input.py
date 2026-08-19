from pathlib import Path
def validate_input(config) :
    print("Starting Input Validation")
    fasta = Path(config["reference"]["fasta"])
    metadata = Path(config["metadata"])
    gtf = Path(config["reference"]["gtf"])

    required_files = {
        "Genome_Fasta" : fasta,
        "Annotation_file" : gtf,
        "Metadata" : metadata
     }


    for key,value in required_files.items():
        if value.exists() == False :
            raise FileNotFoundError(
               f"{key} not found at Path : {value}" 
            )

    print("Input Validation Passed !")