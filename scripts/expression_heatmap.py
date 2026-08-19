import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_expression_heatmap(dds, run_dir):

    output_dir = run_dir / "results/visualization"
    output_dir.mkdir(parents=True, exist_ok=True)


    vst_counts = pd.DataFrame(
        dds.layers["vst_counts"],
        index=dds.obs_names,
        columns=dds.var_names
    )

  
    significant_genes_file = (
        run_dir / "results/deseq/significant_genes.csv"
    )

    significant_genes = pd.read_csv(
        significant_genes_file
    )


    gene_ids = significant_genes["Geneid"].tolist()


    gene_ids = [
        gene for gene in gene_ids
        if gene in vst_counts.columns
    ]

    if not gene_ids:
        print(
        "\nNo significant genes found. "
        "Skipping DEG expression heatmap."
        )
        return

    expression = vst_counts[gene_ids]

   
    expression = expression.T

 
    expression = expression.sub(
        expression.mean(axis=1),
        axis=0
    )

    plt.figure(
        figsize=(
            max(8, len(expression.columns) * 1.2),
            max(8, len(expression.index) * 0.15)
        )
    )

    plt.imshow(
        expression,
        aspect="auto",
        interpolation="nearest"
    )

    plt.colorbar(
        label="VST expression"
    )

    sample_names = expression.columns.tolist()

    plt.xticks(
        range(len(sample_names)),
        sample_names,
        rotation=90
    )

    plt.yticks([])

    plt.xlabel("Samples")
    plt.ylabel("Significant genes")
    plt.title("Expression Heatmap of Significant DEGs")

    plt.tight_layout()

    plt.savefig(
        output_dir / "DEG_expression_heatmap.png",
        dpi=300
    )

    plt.close()

    print("\nDEG expression heatmap completed.")