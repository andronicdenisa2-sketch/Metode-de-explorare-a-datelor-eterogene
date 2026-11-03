#!/usr/bin/env python3
"""CP2 U7 - Pas 2: split temporal, imputare, standardizare fara leakage.
Utilizare: python CP2_U7_preprocesare_date.py --input CP1_X_integrat_2015_2021.csv --output rezultate_pas2
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

FEATURES = ['suprafata_km2', 'temperatura_medie_c', 'precipitatii_totale_mm', 'lst_zi_c', 'lst_noapte_c']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='CSV integrat CP1')
    parser.add_argument('--output', default='rezultate_pas2')
    parser.add_argument('--cutoff', default='2020-01', help='Prima luna din test, YYYY-MM')
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input, encoding='utf-8-sig')
    required = ['lac', 'data'] + FEATURES
    missing_columns = sorted(set(required) - set(df.columns))
    if missing_columns:
        raise ValueError(f'Lipsesc coloanele: {missing_columns}')
    if df[['lac', 'data']].duplicated().any():
        raise ValueError('Exista chei lac/data duplicate!')
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m', errors='raise')
    cutoff = pd.to_datetime(args.cutoff, format='%Y-%m')
    df = df.sort_values(['data', 'lac']).reset_index(drop=True)
    for col in FEATURES:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
    train_mask = df['data'] < cutoff
    test_mask = ~train_mask
    if not train_mask.any() or not test_mask.any():
        raise ValueError('Split invalid: train si test trebuie sa aiba observatii.')
    if df.loc[train_mask, FEATURES].isna().all().any():
        raise ValueError('Cel putin o trasatura este complet lipsa in train.')
    imputer = SimpleImputer(strategy='median', keep_empty_features=True)
    scaler = StandardScaler()
    x_train_imputed = imputer.fit_transform(df.loc[train_mask, FEATURES])
    x_test_imputed = imputer.transform(df.loc[test_mask, FEATURES])
    x_train_scaled = scaler.fit_transform(x_train_imputed)
    x_test_scaled = scaler.transform(x_test_imputed)
    train = df.loc[train_mask, ['lac', 'data']].copy()
    test = df.loc[test_mask, ['lac', 'data']].copy()
    for i, feature in enumerate(FEATURES):
        train[feature] = x_train_scaled[:, i]
        test[feature] = x_test_scaled[:, i]
    train['split'] = 'train'
    test['split'] = 'test'
    combined = pd.concat([train, test], ignore_index=True).sort_values(['data', 'lac'])
    combined['data'] = combined['data'].dt.strftime('%Y-%m')
    combined.to_csv(out / 'CP2_X_standardizat.csv', index=False, encoding='utf-8-sig')
    report = pd.DataFrame({
        'trasatura': FEATURES,
        'lipsa_total': [int(df[c].isna().sum()) for c in FEATURES],
        'lipsa_train': [int(df.loc[train_mask, c].isna().sum()) for c in FEATURES],
        'lipsa_test': [int(df.loc[test_mask, c].isna().sum()) for c in FEATURES],
        'mediana_imputare_train': imputer.statistics_,
        'media_train_dupa_imputare': scaler.mean_,
        'deviatie_standard_train': scaler.scale_,
    })
    report.to_csv(out / 'CP2_raport_preprocesare.csv', index=False, encoding='utf-8-sig')
    summary = pd.DataFrame([
        {'split': 'train', 'n': int(train_mask.sum()), 'prima_luna': df.loc[train_mask, 'data'].min().strftime('%Y-%m'), 'ultima_luna': df.loc[train_mask, 'data'].max().strftime('%Y-%m')},
        {'split': 'test', 'n': int(test_mask.sum()), 'prima_luna': df.loc[test_mask, 'data'].min().strftime('%Y-%m'), 'ultima_luna': df.loc[test_mask, 'data'].max().strftime('%Y-%m')},
    ])
    summary.to_csv(out / 'CP2_split_temporal.csv', index=False, encoding='utf-8-sig')
    print('Split temporal:')
    print(summary.to_string(index=False))
    print('\nValori lipsa si parametri calculati DOAR pe train:')
    print(report.to_string(index=False))
    print(f'\nSalvat in: {out.resolve()}')

if __name__ == '__main__':
    main()
