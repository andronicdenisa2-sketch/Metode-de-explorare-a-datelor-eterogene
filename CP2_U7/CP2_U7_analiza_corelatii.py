r"""CP2 U7 — statistici descriptive si corelatii, pe datele CP1 si CP2.

Rulare din folderul Desktop/CP2:
python CP2_U7_analiza_corelatii.py --input "..\CP1_U7\rezultate\CP1_X_integrat_2015_2021.csv" --standardizat "CP2_U7_date_preprocesate\CP2_X_standardizat.csv" --output "CP2_U7_rezultate_corelatii"
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FEATURES = ['suprafata_km2', 'temperatura_medie_c', 'precipitatii_totale_mm', 'lst_zi_c', 'lst_noapte_c']
LABELS = {'suprafata_km2':'Suprafata apei (km²) — JRC',
          'temperatura_medie_c':'Temperatura aerului (°C) — ERA5-Land',
          'precipitatii_totale_mm':'Precipitatii (mm) — ERA5-Land',
          'lst_zi_c':'LST zi (°C) — MODIS',
          'lst_noapte_c':'LST noapte (°C) — MODIS'}

def heatmap(df, filename, title):
    fig, ax = plt.subplots(figsize=(9, 7))
    vals = df.to_numpy(dtype=float)
    im = ax.imshow(vals, cmap='coolwarm', vmin=-1, vmax=1)
    ax.set_xticks(range(len(df.columns)), [LABELS.get(c,c) for c in df.columns], rotation=40, ha='right', fontsize=8)
    ax.set_yticks(range(len(df.index)), [LABELS.get(c,c) for c in df.index], fontsize=8)
    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            if np.isfinite(vals[i,j]):
                ax.text(j,i,f'{vals[i,j]:.2f}',ha='center',va='center',fontsize=9,
                        color='white' if abs(vals[i,j])>0.65 else 'black')
    fig.colorbar(im, ax=ax, label='Corelatie Pearson')
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(filename,dpi=180,bbox_inches='tight')
    plt.close(fig)

def main():
    ap = argparse.ArgumentParser(description='CP2 U7 — statistici si corelatii')
    ap.add_argument('--input',required=True,help='CSV original integrat CP1')
    ap.add_argument('--standardizat',required=True,help='CSV X standardizat din pasul 2')
    ap.add_argument('--output',default='CP2_U7_rezultate_corelatii')
    args = ap.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    raw=pd.read_csv(args.input); z=pd.read_csv(args.standardizat)
    required={'lac','data',*FEATURES}
    for name,df in [('CP1',raw),('CP2',z)]:
        missing=required-set(df.columns)
        if missing: raise ValueError(f'{name}: coloane lipsa: {sorted(missing)}')
        if df.duplicated(['lac','data']).any(): raise ValueError(f'{name}: chei lac + data duplicate')
    if 'split' not in z.columns: raise ValueError('Matricea standardizata nu contine coloana split')
    if set(map(tuple,raw[['lac','data']].to_numpy()))!=set(map(tuple,z[['lac','data']].to_numpy())):
        raise ValueError('Cheile lac + data nu coincid intre CP1 si CP2')
    raw['data']=pd.to_datetime(raw['data'].astype(str),format='%Y-%m',errors='raise')
    z['data']=pd.to_datetime(z['data'].astype(str),format='%Y-%m',errors='raise')
    for f in FEATURES:
        raw[f]=pd.to_numeric(raw[f],errors='raise')
        z[f]=pd.to_numeric(z[f],errors='raise')
    if z[FEATURES].isna().any().any(): raise ValueError('Matricea X standardizata contine NaN')

    # Statistici in unitati fizice: NU imputam valorile originale pentru raportarea distributiilor.
    rows=[]
    for lake,part in [('TOATE',raw),*list(raw.groupby('lac'))]:
        for f in FEATURES:
            s=part[f].dropna()
            rows.append({'lac':lake,'sursa':('JRC' if f=='suprafata_km2' else 'ERA5-Land' if f in FEATURES[1:3] else 'MODIS'),
                         'trasatura':f,'n_disponibile':len(s),'n_lipsa':int(part[f].isna().sum()),
                         'medie':s.mean(),'mediana':s.median(),'std':s.std(),'min':s.min(),
                         'q25':s.quantile(.25),'q75':s.quantile(.75),'max':s.max()})
    pd.DataFrame(rows).to_csv(out/'CP2_statistici_descriptive.csv',index=False,float_format='%.6f')

    # Pearson pe observatii brute complete per pereche (pairwise deletion).
    corr=raw[FEATURES].corr(method='pearson',min_periods=3)
    corr.to_csv(out/'CP2_corelatii_pearson_original.csv',float_format='%.6f')
    heatmap(corr,out/'CP2_harta_corelatii.png','Corelatii Pearson — date originale, toate lacurile')
    for lake,part in raw.groupby('lac'):
        c=part[FEATURES].corr(method='pearson',min_periods=3)
        safe=''.join(x if x.isalnum() or x in '-_' else '_' for x in str(lake))
        c.to_csv(out/f'CP2_corelatii_{safe}.csv',float_format='%.6f')
        heatmap(c,out/f'CP2_harta_corelatii_{safe}.png',f'Corelatii Pearson — {lake}')

    # Verificare distincta a corelatiilor pe train dupa imputare si standardizare.
    train=z[z['split']=='train']
    train[FEATURES].corr().to_csv(out/'CP2_corelatii_train_standardizat.csv',float_format='%.6f')

    for f in FEATURES:
        fig,ax=plt.subplots(figsize=(8,4.8))
        for lake,part in raw.groupby('lac'):
            vals=part[f].dropna()
            if len(vals): ax.hist(vals,bins=12,alpha=.5,label=f'{lake} (n={len(vals)})')
        ax.set_xlabel(LABELS[f]);ax.set_ylabel('Numar de observatii')
        ax.set_title('Distributia pe lacuri');ax.legend();fig.tight_layout()
        fig.savefig(out/f'CP2_distributie_{f}.png',dpi=180)
        plt.close(fig)

    coverage=raw.groupby('lac').agg(observatii=('data','size'),prima_luna=('data','min'),ultima_luna=('data','max'))
    coverage['prima_luna']=coverage['prima_luna'].dt.strftime('%Y-%m')
    coverage['ultima_luna']=coverage['ultima_luna'].dt.strftime('%Y-%m')
    coverage.to_csv(out/'CP2_acoperire_pe_lac.csv')
    print('\nANALIZA CP2 — FINALIZATA')
    print(f'Observatii: {len(raw)} | Lacuri: {raw.lac.nunique()} | Trasaturi: {len(FEATURES)}')
    print('Valori lipsa in datele originale:',raw[FEATURES].isna().sum().to_dict())
    print('Corelatii Pearson cu suprafata apei (date brute, perechi disponibile):')
    print(corr['suprafata_km2'].round(3).to_string())
    print(f'Fisiere salvate in: {out.resolve()}')
    print('NOTA: corelatiile sunt descriptive, nu indica relatii cauzale.')

if __name__=='__main__': main()
