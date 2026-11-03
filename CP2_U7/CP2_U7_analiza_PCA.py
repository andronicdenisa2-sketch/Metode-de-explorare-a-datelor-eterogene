#!/usr/bin/env python3
"""CP2 U7 - PCA pe matricea standardizata din pasul 2, fara leakage.
Exemplu:
 python CP2_U7_analiza_PCA.py --input "CP2_U7_date_preprocesate/CP2_X_standardizat.csv" --output "CP2_U7_rezultate_PCA"
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

FEATURES = ['suprafata_km2', 'temperatura_medie_c', 'precipitatii_totale_mm', 'lst_zi_c', 'lst_noapte_c']
LABELS = ['Suprafata JRC', 'Temp. aer ERA5', 'Precipitatii ERA5', 'LST zi MODIS', 'LST noapte MODIS']

def main():
    p = argparse.ArgumentParser(description='Analiza PCA CP2 U7')
    p.add_argument('--input', required=True, help='CP2_X_standardizat.csv generat la pasul 2')
    p.add_argument('--output', default='CP2_U7_rezultate_PCA')
    args = p.parse_args()
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input, encoding='utf-8-sig')
    needed = ['lac','data','split'] + FEATURES
    missing = [c for c in needed if c not in df.columns]
    if missing: raise ValueError(f'Lipsesc coloanele: {missing}')
    if df[['lac','data']].duplicated().any(): raise ValueError('Chei lac/data duplicate')
    if df[FEATURES].isna().any().any(): raise ValueError('Exista valori lipsa; ruleaza intai preprocesarea')
    if not np.isfinite(df[FEATURES].to_numpy(dtype=float)).all(): raise ValueError('Valori infinite sau invalide')
    if not set(df['split'].unique()).issubset({'train','test'}): raise ValueError('split trebuie sa fie train/test')
    train = df['split'].eq('train'); test = df['split'].eq('test')
    if train.sum() < 3 or test.sum() < 1: raise ValueError('Split invalid')
    Xtr = df.loc[train,FEATURES].to_numpy(dtype=float)
    Xte = df.loc[test,FEATURES].to_numpy(dtype=float)
    # PCA antrenata EXCLUSIV pe train; transformarea test nu modifica modelul.
    model = PCA(n_components=len(FEATURES), svd_solver='full').fit(Xtr)
    ztr = model.transform(Xtr); zte = model.transform(Xte)
    components = [f'PC{i+1}' for i in range(len(FEATURES))]
    variance = pd.DataFrame({'componenta': components,
       'varianta_explicata': model.explained_variance_ratio_,
       'varianta_explicata_pct': model.explained_variance_ratio_*100,
       'varianta_cumulata_pct': np.cumsum(model.explained_variance_ratio_)*100})
    variance.to_csv(out/'CP2_PCA_varianta_explicata.csv', index=False, encoding='utf-8-sig')
    loadings = pd.DataFrame(model.components_.T, index=FEATURES, columns=components)
    loadings.index.name='trasatura'
    loadings.to_csv(out/'CP2_PCA_coeficienti_componente.csv', encoding='utf-8-sig')
    contribution = pd.DataFrame(model.components_.T**2*100, index=FEATURES, columns=components)
    contribution.index.name='trasatura'
    contribution.to_csv(out/'CP2_PCA_contributii_pct.csv', encoding='utf-8-sig')
    scores = df[['lac','data','split']].copy()
    for i, name in enumerate(components):
        scores[name] = np.nan
        scores.loc[train,name] = ztr[:,i]
        scores.loc[test,name] = zte[:,i]
    scores.to_csv(out/'CP2_PCA_proiectie_lac_luna.csv', index=False, encoding='utf-8-sig')
    # Baseline nesupravegheat: eroarea de reconstructie cu primele doua PC.
    # Nu este un scor de predictie a suprafetei lacurilor.
    rows=[]
    for label, X, Z in [('train',Xtr,ztr),('test',Xte,zte)]:
        for k in [1,2,3,4,5]:
            rec = Z[:,:k] @ model.components_[:k,:] + model.mean_
            rows.append({'split':label,'n':len(X),'componente':k,
                         'mse_reconstructie_standardizat':float(np.mean((X-rec)**2)),
                         'rmse_reconstructie_standardizat':float(np.sqrt(np.mean((X-rec)**2)))})
    pd.DataFrame(rows).to_csv(out/'CP2_PCA_eroare_reconstructie.csv',index=False,encoding='utf-8-sig')
    fig,ax=plt.subplots(figsize=(8,5))
    ax.bar(components, variance['varianta_explicata_pct'], label='Individuala')
    ax.plot(components, variance['varianta_cumulata_pct'], marker='o', label='Cumulata')
    ax.set(ylabel='Varianta explicata (%)',xlabel='Componenta principala',title='PCA - varianta explicata (model antrenat pe train)',ylim=(0,105))
    ax.legend(); fig.tight_layout(); fig.savefig(out/'CP2_PCA_varianta_explicata.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5))
    pos=np.arange(len(FEATURES)); w=.36
    ax.bar(pos-w/2,contribution['PC1'],width=w,label='PC1')
    ax.bar(pos+w/2,contribution['PC2'],width=w,label='PC2')
    ax.set_xticks(pos, LABELS, rotation=22,ha='right')
    ax.set(ylabel='Contributie (%)',title='Contributia trasaturilor la PC1 si PC2');ax.legend()
    fig.tight_layout();fig.savefig(out/'CP2_PCA_contributii.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,6))
    colors=plt.get_cmap('tab10')
    for j,lac in enumerate(sorted(scores['lac'].unique())):
        for split,marker in [('train','o'),('test','x')]:
            sub=scores[(scores.lac==lac)&(scores.split==split)]
            if len(sub):ax.scatter(sub.PC1,sub.PC2,label=f'{lac} ({split})',marker=marker,alpha=.7,color=colors(j))
    ax.axhline(0,color='gray',linewidth=.7);ax.axvline(0,color='gray',linewidth=.7)
    ax.set(xlabel=f'PC1 ({variance.iloc[0].varianta_explicata_pct:.1f}%)',
           ylabel=f'PC2 ({variance.iloc[1].varianta_explicata_pct:.1f}%)',title='Proiectie PCA - lac × luna')
    ax.legend(fontsize=8);fig.tight_layout();fig.savefig(out/'CP2_PCA_proiectie_PC1_PC2.png',dpi=180);plt.close(fig)
    print(f'Observatii: train={train.sum()}, test={test.sum()}')
    print(variance.to_string(index=False,float_format=lambda x:f'{x:.3f}'))
    print('\nContributii PC1/PC2 (%):')
    print(contribution[['PC1','PC2']].round(2).to_string())
    print('\nRezultate salvate in:',out.resolve())

if __name__=='__main__': main()
