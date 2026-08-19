from pathlib import Path
import pandas as pd

def filter_significant_genes(run_dir) :
    deseq_file = Path(run_dir/"results/deseq/deseq_results.csv")
    out_dir = Path(run_dir/"results/deseq")
    out_dir.mkdir(parents=True,exist_ok=True)

    results = pd.read_csv(deseq_file, index_col=0)
    results.index.name = "Geneid"

    significant_genes = results[(results['padj'] < 0.05) & (results["log2FoldChange"].abs() >1)]

    output_file = out_dir / "significant_genes.csv"

    significant_genes.to_csv(output_file)

    print(f"File saves Successfully!\nFound {len(significant_genes)} significant genes")


