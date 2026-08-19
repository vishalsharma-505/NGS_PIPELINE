import pandas as pd
import matplotlib.pyplot as plt


def plot_sample_correlation(dds, run_dir):

    output_dir = run_dir / "results/visualization"
    output_dir.mkdir(parents=True, exist_ok=True)

    vst_counts = pd.DataFrame(
        dds.layers["vst_counts"],
        index=dds.obs_names,
        columns=dds.var_names
    )


    correlation_matrix = vst_counts.T.corr()

    plt.figure(figsize=(8, 7))

    plt.imshow(
        correlation_matrix,
        aspect="auto",
        interpolation="nearest"
    )

    plt.colorbar(label="Pearson correlation")

    sample_names = correlation_matrix.columns.tolist()

    plt.xticks(
    range(len(sample_names)),
    sample_names,
    rotation=90
    )

    plt.yticks(
    range(len(sample_names)),
    sample_names
    )

    plt.title("Sample Correlation Heatmap")
    plt.xlabel("Samples")
    plt.ylabel("Samples")

    plt.tight_layout()

    plt.savefig(
        output_dir / "sample_correlation_heatmap.png",
        dpi=300
    )

    plt.close()

    print("\nSample correlation heatmap completed.")