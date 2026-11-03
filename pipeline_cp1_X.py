"""Pipeline reproductibil CP1: JRC + ERA5-Land + MODIS -> X optic si X integrat.
Rule QC: JRC >= 90%; schimbari >30% doar semnalate; lipsurile nu devin zero.
Rule scaling: valorile CP1 raman brute; scaler se ajusteaza doar pe train in CP2.
Executie: python pipeline_cp1_X.py (din directorul proiectului CP1_U7).
Intrari: date_originale/*.csv; iesiri: rezultate/*.csv.
"""
import csv
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent
INPUT_DIR = BASE / 'date_originale'
OUTPUT_DIR = BASE / 'rezultate'
SOURCES = {
    'jrc': ('CP1_JRC_Lacuri_2015_2021.csv', ['suprafata_km2', 'arie_valida_km2', 'acoperire_date_pct', 'arie_zona_km2']),
    'era5': ('CP1_ERA5_Lacuri_2015_2021.csv', ['temperatura_medie_c', 'precipitatii_totale_mm']),
    'modis': ('CP1_MODIS_LST_2015_2021.csv', ['lst_zi_c', 'lst_noapte_c', 'numar_imagini_modis']),
}
KEYS = ('lac', 'data')
FEATURES = ['suprafata_km2', 'temperatura_medie_c', 'precipitatii_totale_mm', 'lst_zi_c', 'lst_noapte_c']

def read_source(filename, fields):
    indexed = {}
    with (INPUT_DIR / filename).open(encoding='utf-8-sig', newline='') as file:
        for row in csv.DictReader(file):
            key = tuple(row[k].strip() for k in KEYS)
            if key in indexed:
                raise ValueError(f'Duplicat {filename}: {key}')
            indexed[key] = {k: row.get(k, '').strip() for k in fields}
    return indexed

def number(s):
    return None if s == '' else float(s)

def write_csv(name, rows, columns):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUTPUT_DIR / name).open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows([{c: row.get(c, '') for c in columns} for row in rows])

sources = {name: read_source(filename, fields) for name, (filename, fields) in SOURCES.items()}
key_sets = [set(v) for v in sources.values()]
if not all(s == key_sets[0] for s in key_sets[1:]):
    raise ValueError('Sursele nu au aceleasi chei lac/data. Verificati lunile lipsa.')

all_rows = []
for lac, data in sorted(key_sets[0]):
    row = {'lac': lac, 'data': data}
    for name in SOURCES:
        row.update(sources[name][(lac, data)])
    area = number(row['suprafata_km2'])
    coverage = number(row['acoperire_date_pct'])
    good = area is not None and coverage is not None and coverage >= 90
    row['jrc_valid_90_pct'] = 'DA' if good else 'NU'
    row['suprafata_filtrata_km2'] = row['suprafata_km2'] if good else ''
    row['schimbare_peste_30_pct'] = 'NEEVALUABIL'
    row['variatie_lunara_pct'] = ''
    all_rows.append(row)

# Schimbarea se calculeaza numai pentru doua luni consecutive, ambele valide.
previous = {}
for row in all_rows:
    lake, date = row['lac'], row['data']
    prev = previous.get(lake)
    if prev and row['jrc_valid_90_pct'] == 'DA' and prev['jrc_valid_90_pct'] == 'DA':
        year, month = map(int, prev['data'].split('-'))
        next_month = f'{year + (month == 12):04d}-{month % 12 + 1:02d}'
        prev_area = number(prev['suprafata_filtrata_km2'])
        if date == next_month and prev_area and prev_area > 0:
            delta = 100 * (number(row['suprafata_filtrata_km2']) - prev_area) / prev_area
            row['variatie_lunara_pct'] = f'{delta:.4f}'
            row['schimbare_peste_30_pct'] = 'DA' if abs(delta) > 30 else 'NU'
    previous[lake] = row

valid_rows = [r for r in all_rows if r['jrc_valid_90_pct'] == 'DA']
# X optic = o singura trasatura, X integrat = 5 trasaturi brute; pastram NA pentru LST noapte.
X_optic = [{'lac': r['lac'], 'data': r['data'], 'suprafata_km2': r['suprafata_filtrata_km2']} for r in valid_rows]
X_integrat = []
for r in valid_rows:
    new = {'lac': r['lac'], 'data': r['data']}
    new.update({f: r['suprafata_filtrata_km2'] if f == 'suprafata_km2' else r[f] for f in FEATURES})
    X_integrat.append(new)

write_csv('CP1_X_optic_2015_2021.csv', X_optic, ['lac', 'data', 'suprafata_km2'])
write_csv('CP1_X_integrat_2015_2021.csv', X_integrat, ['lac', 'data'] + FEATURES)
write_csv('CP1_Date_QC_pipeline.csv', all_rows, ['lac', 'data'] + sum((v[1] for v in SOURCES.values()), []) + ['jrc_valid_90_pct', 'suprafata_filtrata_km2', 'variatie_lunara_pct', 'schimbare_peste_30_pct'])

print('Date brute:', len(all_rows))
print('X optic:', len(X_optic), 'x 1')
print('X integrat:', len(X_integrat), 'x 5')
print('Observatii valide pe lac:', dict(Counter(r['lac'] for r in valid_rows)))
print('Lipsuri in X integrat:', {f: sum(not r[f] for r in X_integrat) for f in FEATURES})
print('Variatii >30%:', sum(r['schimbare_peste_30_pct'] == 'DA' for r in all_rows))
