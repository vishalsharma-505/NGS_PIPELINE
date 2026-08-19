from pathlib import Path
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

def run_deseq2(config,run_dir) :
    counts_file = Path(run_dir/"results/counts/gene_counts.txt")
    metadata_file = Path(config["metadata"])

    out_dir = Path(run_dir/"results/deseq")
    out_dir.mkdir(parents=True,exist_ok=True)

    counts = pd.read_csv(counts_file,sep="\t",comment="#")
    counts = counts.set_index("Geneid")

  
    counts = counts.iloc[:,5:]

   

    new_names = [] 

    for sample in counts.columns :
        name = Path(sample).stem  

        name = name.replace(".sorted","") 
        new_names.append(name) 

    counts.columns = new_names  

    metadata = pd.read_csv(metadata_file) 
    metadata = metadata.set_index("sample")

    missing_samples =[]

    for sample in counts.columns :
        if sample not in metadata.index :
            missing_samples.append(sample)

    if missing_samples :
        raise ValueError(
            f"Metadata is missing samples :{','.join(missing_samples)}"
        )

    extra_samples = []

    for sample in metadata.index :
        if sample not in counts.columns :
            extra_samples.append(sample)


    if extra_samples :
        raise ValueError(
            f"Metadata contains extra samples :{','.join(extra_samples)}"
        )
    rearrange_samples = counts.columns
    metadata = metadata.loc[rearrange_samples] 
    
    counts = counts.T 

    dds = DeseqDataSet(
        counts= counts,
        metadata= metadata,
        design= "~ condition" 
    )

    dds.deseq2()
    dds.vst()

    conditions = metadata["condition"].unique()

    if len(conditions) != 2:
        raise ValueError(
            f"DESeq2 requires exactly 2 conditions, "
            f"but found: {', '.join(conditions)}"
        )

    reference = conditions[0]
    comparison = conditions[1]

    stats = DeseqStats(
        dds,
        contrast=["condition", comparison, reference]
    )
    stats.summary()
    results = stats.results_df

    results.to_csv(out_dir/"deseq_results.csv")

    print("\nDeSeq Analysis completed ")
    return dds, results
