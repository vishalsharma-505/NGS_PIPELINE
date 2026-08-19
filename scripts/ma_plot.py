from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def plot_ma(results, run_dir):

    output_dir = run_dir / "results/visualization"
    output_dir.mkdir(parents=True, exist_ok=True)

    required_columns = [
        "baseMean",
        "log2FoldChange",
        "padj"
    ]

    for column in required_columns:
        if column not in results.columns:
            raise ValueError(
                f"Required column '{column}' not found in DESeq2 results"
            )

    ma_data = results[
        ["baseMean", "log2FoldChange", "padj"]
    ].dropna()

    ma_data = ma_data[ma_data["baseMean"] > 0]

    significant = ma_data["padj"] < 0.05
    non_significant = ~significant

    plt.figure(figsize=(8, 6))

    plt.scatter(
        ma_data.loc[non_significant, "baseMean"],
        ma_data.loc[non_significant, "log2FoldChange"],
        s=8,
        alpha=0.5
    )

    plt.scatter(
        ma_data.loc[significant, "baseMean"],
        ma_data.loc[significant, "log2FoldChange"],
        s=10,
        alpha=0.7
    )

    plt.xscale("log")

    plt.axhline(
        y=0,
        linestyle="--",
        linewidth=1
    )

    plt.xlabel("Mean expression (baseMean)")
    plt.ylabel("log2 Fold Change")
    plt.title("MA Plot")

    plt.tight_layout()

    plt.savefig(
        output_dir / "MA_plot.png",
        dpi=300
    )

    plt.close()

    print("\nMA plot completed.")