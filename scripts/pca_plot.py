from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def plot_pca(dds, run_dir):

    output_dir = run_dir / "results/visualization"
    output_dir.mkdir(parents=True, exist_ok=True)

    vst_counts = pd.DataFrame(
        dds.layers["vst_counts"],
        index=dds.obs_names,
        columns=dds.var_names
    )

    pca = PCA(n_components=2)

    components = pca.fit_transform(vst_counts)

    pca_df = pd.DataFrame(
        components,
        index=vst_counts.index,
        columns=["PC1", "PC2"]
    )

    pca_df["condition"] = dds.obs["condition"].values

    plt.figure(figsize=(7, 6))

    for condition in pca_df["condition"].unique():

        subset = pca_df[pca_df["condition"] == condition]

        plt.scatter(
            subset["PC1"],
            subset["PC2"],
            label=condition
        )

    plt.xlabel(
        f"PC1 ({pca.explained_variance_ratio_[0] * 100:.1f}%)"
    )

    plt.ylabel(
        f"PC2 ({pca.explained_variance_ratio_[1] * 100:.1f}%)"
    )

    plt.title("PCA of RNA-seq samples")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        output_dir / "PCA.png",
        dpi=300
    )

    plt.close()

    print("\nPCA plot completed.")