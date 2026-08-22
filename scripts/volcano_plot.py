from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_volcano(results, run_dir):

    output_dir = run_dir / "results/visualization"
    output_dir.mkdir(parents=True, exist_ok=True)

    required_columns = [
        "log2FoldChange",
        "padj"
    ]

    for column in required_columns:
        if column not in results.columns:
            raise ValueError(
                f"Required column '{column}' not found in DESeq2 results"
            )

    volcano_data = results[
        ["log2FoldChange", "padj"]
    ].copy()

    volcano_data = volcano_data.dropna()
    


    volcano_data["padj"] = volcano_data["padj"].replace(0, 1e-300)

    volcano_data["neg_log10_padj"] = -np.log10(
        volcano_data["padj"]
    )

    significant = volcano_data["padj"] < 0.05
    non_significant = ~significant

    plt.figure(figsize=(8, 6))

    plt.scatter(
        volcano_data.loc[non_significant, "log2FoldChange"],
        volcano_data.loc[non_significant, "neg_log10_padj"],
        s=8,
        alpha=0.5
    )

    plt.scatter(
        volcano_data.loc[significant, "log2FoldChange"],
        volcano_data.loc[significant, "neg_log10_padj"],
        s=10,
        alpha=0.7
    )

    plt.axhline(
        y=-np.log10(0.05),
        linestyle="--",
        linewidth=1
    )

    plt.xlabel("log2 Fold Change")
    plt.ylabel("-log10 Adjusted p-value")
    plt.title("Volcano Plot")

    plt.tight_layout()

    plt.savefig(
        output_dir / "volcano_plot.png",
        dpi=300
    )

    plt.close()

    print("\nVolcano plot completed.")
