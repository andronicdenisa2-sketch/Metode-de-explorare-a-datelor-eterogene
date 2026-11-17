#!/usr/bin/env python3
"""CP3 U7 – comparatie PCA vs t-SNE si stabilitate (doar train).
Exemplu:
python CP3_U7_tSNE_stabilitate.py --input "../CP2/CP2_U7_date_preprocesate/CP2_X_standardizat.csv" --output "CP3_U7_rezultate/tSNE"
"""
import argparse
import inspect
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, trustworthiness

GROUPS = {
    'ERA5_Land': ['temperatura_medie_c', 'precipitatii_totale_mm'],
    'MODIS': ['lst_zi_c', 'lst_noapte_c'],
    'Combinate': ['suprafata_km2', 'temperatura_medie_c', 'precipitatii_totale_mm', 'lst_zi_c', 'lst_noapte_c'],
}
SEEDS = (42, 123, 2026)

def tsne_fit(x, seed):
    n = len(x)
    perplexity = min(15, max(2, (n-1)//3))
    kwargs = dict(n_components=2, perplexity=perplexity, random_state=seed,
                  init='random', learning_rate='auto', method='barnes_hut')
    # Compatibilitate intre versiuni sklearn
    kw = 'max_iter' if 'max_iter' in inspect.signature(TSNE).parameters else 'n_iter'
    kwargs[kw] = 1000
    return TSNE(**kwargs).fit_transform(x), perplexity

def analyze(df, group, cols, period, output):
    x = df[cols].to_numpy(float)
    n = len(df)
    if n < 10:
        print(f'Sar peste {group}/{period}: doar {n} observatii')
        return []
    # trustworthiness necesita n_neighbors < n/2 si < n/3 pentru implementari sklearn
    neighbors = min(5, max(2, (n-1)//4))
    pca = PCA(n_components=2, svd_solver='full')
    zp = pca.fit_transform(x)
    results = [dict(grup=group, perioada=period, metoda='PCA', seed='determinist',
                    n=n, n_trasaturi=len(cols), n_neighbors=neighbors,
                    perplexity=np.nan, trustworthiness=trustworthiness(x, zp, n_neighbors=neighbors),
                    varianta_explicata_pct=100*pca.explained_variance_ratio_.sum())]
    for seed in SEEDS:
        z, perp = tsne_fit(x, seed)
        score = trustworthiness(x, z, n_neighbors=neighbors)
        results.append(dict(grup=group, perioada=period, metoda='t-SNE', seed=seed,
                            n=n, n_trasaturi=len(cols), n_neighbors=neighbors,
                            perplexity=perp, trustworthiness=score,
                            varianta_explicata_pct=np.nan))
        if period == 'train_complet' and seed == SEEDS[0]:
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            for ax, points, label in [(axes[0], zp, 'PCA'), (axes[1], z, 't-SNE')]:
                for lake in sorted(df['lac'].unique()):
                    mask = df['lac'].eq(lake).to_numpy()
                    ax.scatter(points[mask, 0], points[mask, 1], label=lake, alpha=.7, s=30)
                ax.set_title(f'{label} – {group}')
                ax.set_xlabel('Componenta 1' if label == 'PCA' else 't-SNE 1')
                ax.set_ylabel('Componenta 2' if label == 'PCA' else 't-SNE 2')
                ax.legend(fontsize=8)
            fig.suptitle('Proiectii 2D pe train – axele nu sunt comparabile direct')
            fig.tight_layout()
            fig.savefig(output/f'CP3_comparatie_PCA_tSNE_{group}.png', dpi=170)
            plt.close(fig)
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', default='CP3_U7_rezultate/tSNE')
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input, encoding='utf-8-sig')
    needed = ['lac', 'data', 'split'] + list(dict.fromkeys(c for cols in GROUPS.values() for c in cols))
    missing = [c for c in needed if c not in df]
    if missing:
        raise ValueError(f'Coloane lipsa: {missing}')
    df['data'] = pd.to_datetime(df['data'])
    train = df[df['split'].eq('train')].copy()
    if len(train) != 99:
        print(f'Atentie: train are {len(train)} observatii, nu 99.')
    if train[needed[3:]].isna().any().any():
        raise ValueError('Valori lipsa in train')
    results = []
    for group, cols in GROUPS.items():
        # Test de stabilitate pe subperioade, doar train; fara a amesteca testul
        periods = {
            'train_complet': train,
            '2015_2017': train[train['data'] < '2018-01-01'],
            '2018_2019': train[train['data'] >= '2018-01-01'],
        }
        for period, subset in periods.items():
            results.extend(analyze(subset, group, cols, period, out))
    result = pd.DataFrame(results)
    result.to_csv(out/'CP3_PCA_tSNE_metrici.csv', index=False, encoding='utf-8-sig')
    summary = (result[result['metoda'].eq('t-SNE')]
               .groupby(['grup', 'perioada'], as_index=False)
               .agg(trustworthiness_medie=('trustworthiness', 'mean'),
                    trustworthiness_std=('trustworthiness', 'std'),
                    n_rulari=('trustworthiness', 'size')))
    summary.to_csv(out/'CP3_tSNE_stabilitate.csv', index=False, encoding='utf-8-sig')
    print('PCA vs t-SNE – train complet:')
    print(result[result['perioada'].eq('train_complet')][['grup','metoda','seed','trustworthiness']].to_string(index=False))
    print('\nStabilitate t-SNE (medie si abatere standard):')
    print(summary.to_string(index=False))
    print(f'\nFisiere salvate in: {out.resolve()}')
    print('NOTA: JRC este unidimensional si nu permite proiectie 2D informativa.')
    print('NOTA: Pentru ERA5 si MODIS, PCA cu 2 componente pastreaza toate dimensiunile initiale.')
    print('NOTA: t-SNE nu are varianta explicata sau reconstrucție inversa standard.')

if __name__ == '__main__':
    main()
