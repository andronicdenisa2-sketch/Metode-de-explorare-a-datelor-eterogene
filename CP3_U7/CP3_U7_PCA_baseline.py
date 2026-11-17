#!/usr/bin/env python3
"""CP3 U7 – Pasul 2: PCA baseline separat pe surse și pe datele combinate.
Exemplu:
python CP3_U7_PCA_baseline.py --input "../CP2/CP2_U7_date_preprocesate/CP2_X_standardizat.csv" --output "CP3_U7_rezultate/PCA"
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

GROUPS = {
    "JRC": ["suprafata_km2"],
    "ERA5_Land": ["temperatura_medie_c", "precipitatii_totale_mm"],
    "MODIS": ["lst_zi_c", "lst_noapte_c"],
    "Combinate": ["suprafata_km2", "temperatura_medie_c",
                  "precipitatii_totale_mm", "lst_zi_c", "lst_noapte_c"],
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="CSV-ul standardizat din CP2")
    ap.add_argument("--output", default="CP3_U7_rezultate/PCA")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input, encoding="utf-8-sig")
    features = GROUPS["Combinate"]
    required = ["lac", "data", "split"] + features
    absent = [x for x in required if x not in df.columns]
    if absent:
        raise ValueError(f"Coloane lipsa: {absent}")
    if df[["lac", "data"]].duplicated().any():
        raise ValueError("Exista observatii duplicate lac/data.")
    if df[features].isna().any().any() or not np.isfinite(df[features].to_numpy(float)).all():
        raise ValueError("Date lipsa sau nefinite in matricea CP2.")
    if set(df["split"].unique()) != {"train", "test"}:
        raise ValueError("Coloana split trebuie sa contina train si test.")
    tr = df["split"].eq("train")
    te = df["split"].eq("test")
    if tr.sum() < 3 or te.sum() < 1:
        raise ValueError("Prea putine observatii train/test.")
    print(f"Date incarcate: {len(df)} observatii; train={tr.sum()}, test={te.sum()}")
    metrics, variances, loadings = [], [], []
    for name, cols in GROUPS.items():
        xtr = df.loc[tr, cols].to_numpy(float)
        xte = df.loc[te, cols].to_numpy(float)
        n_features = len(cols)
        # JRC are o singura variabila: PCA 1D, nu proiectie 2D.
        model = PCA(n_components=n_features, svd_solver="full").fit(xtr)
        for i, ratio in enumerate(model.explained_variance_ratio_, start=1):
            variances.append({"grup": name, "componenta": f"PC{i}",
                              "varianta_explicata_pct": 100*float(ratio),
                              "varianta_cumulata_pct": 100*float(
                                  np.sum(model.explained_variance_ratio_[:i]))})
        for j, col in enumerate(cols):
            for i in range(n_features):
                loadings.append({"grup": name, "trasatura": col,
                                 "componenta": f"PC{i+1}",
                                 "coeficient": float(model.components_[i, j]),
                                 "contributie_pct": float(100*model.components_[i, j]**2)})
        for subset, x in [("train", xtr), ("test", xte)]:
            z = model.transform(x)
            for k in range(1, n_features+1):
                rec = z[:, :k] @ model.components_[:k, :] + model.mean_
                rmse = float(np.sqrt(np.mean((x-rec)**2)))
                metrics.append({"grup": name, "split": subset, "n": len(x),
                                "n_trasaturi": n_features, "n_componente": k,
                                "rmse_reconstructie_standardizat": rmse,
                                "varianta_explicata_train_pct": float(
                                    100*np.sum(model.explained_variance_ratio_[:k]))})
        # Proiectie train/test pe primele doua componente, doar pentru grupurile >=2D.
        if n_features >= 2:
            z = model.transform(df[cols].to_numpy(float))[:, :2]
            fig, ax = plt.subplots(figsize=(8, 5))
            for lake in sorted(df["lac"].unique()):
                for subset, marker in [("train", "o"), ("test", "x")]:
                    sel = df["lac"].eq(lake) & df["split"].eq(subset)
                    ax.scatter(z[sel, 0], z[sel, 1], marker=marker,
                               alpha=.7, label=f"{lake} ({subset})")
            ax.set_xlabel(f"PC1 ({100*model.explained_variance_ratio_[0]:.1f}%)")
            ax.set_ylabel(f"PC2 ({100*model.explained_variance_ratio_[1]:.1f}%)")
            ax.set_title(f"PCA – {name} (model ajustat pe train)")
            ax.legend(fontsize=8, ncol=2)
            fig.tight_layout()
            fig.savefig(out/f"CP3_PCA_proiectie_{name}.png", dpi=170)
            plt.close(fig)
        print(f"{name}: {n_features} trasaturi, "
              f"PC1={100*model.explained_variance_ratio_[0]:.2f}%")
    pd.DataFrame(metrics).to_csv(out/"CP3_PCA_comparatie_RMSE.csv",
                                  index=False, encoding="utf-8-sig")
    pd.DataFrame(variances).to_csv(out/"CP3_PCA_varianta_explicata.csv",
                                    index=False, encoding="utf-8-sig")
    pd.DataFrame(loadings).to_csv(out/"CP3_PCA_coeficienti_contributii.csv",
                                   index=False, encoding="utf-8-sig")
    # Grafic comparativ: numarul maxim de componente difera intre surse.
    fig, ax = plt.subplots(figsize=(9, 5))
    v = pd.DataFrame(variances)
    for name, part in v.groupby("grup", sort=False):
        ax.plot(range(1, len(part)+1), part["varianta_cumulata_pct"],
                marker="o", label=name)
    ax.set(xlabel="Numar componente PCA",
           ylabel="Varianta cumulata explicata pe train (%)",
           title="CP3 – PCA baseline: surse separate vs combinate",
           ylim=(0, 105))
    ax.legend()
    ax.grid(alpha=.2)
    fig.tight_layout()
    fig.savefig(out/"CP3_PCA_comparatie_varianta.png", dpi=170)
    plt.close(fig)
    print(f"Rezultate salvate in: {out.resolve()}")
    print("NOTA: RMSE se compara intre grupuri cu prudenta: "
          "dimensionalitatea si continutul variabilelor difera.")

if __name__ == "__main__":
    main()
