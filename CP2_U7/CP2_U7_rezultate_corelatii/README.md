# CP2 – Analiza descriptivă și corelațiile

## 1. Obiectiv

Această etapă urmărește analiza distribuțiilor și identificarea relațiilor statistice dintre suprafața apei și factorii meteorologici pentru lacurile Techirghiol, Amara și Nuntași.

Analiza este realizată pentru perioada 2015–2021, utilizând date integrate din JRC Global Surface Water, ERA5-Land și MODIS LST.

## 2. Date utilizate

Matricea finală conține **139 observații lac × lună și 5 trăsături numerice**:

| Variabilă | Sursă | Unitate |
|---|---|---|
| Suprafața apei | JRC | km² |
| Temperatura medie a aerului | ERA5-Land | °C |
| Precipitații totale lunare | ERA5-Land | mm |
| Temperatura suprafeței terestre – zi | MODIS LST | °C |
| Temperatura suprafeței terestre – noapte | MODIS LST | °C |

Distribuția observațiilor valide:

| Lac | Observații |
|---|---:|
| Amara | 51 |
| Nuntași | 43 |
| Techirghiol | 45 |
| **Total** | **139** |

## 3. Analiza descriptivă

Au fost calculate statistici descriptive pentru cele cinci variabile și au fost generate histograme pentru examinarea distribuțiilor.

Fișierul `CP2_statistici_descriptive.csv` conține indicatorii descriptivi calculați.

Graficele disponibile sunt:

- `CP2_distributie_suprafata_km2.png`
- `CP2_distributie_temperatura_medie_c.png`
- `CP2_distributie_precipitatii_totale_mm.png`
- `CP2_distributie_lst_zi_c.png`
- `CP2_distributie_lst_noapte_c.png`

Aceste reprezentări permit examinarea variabilității datelor și identificarea eventualelor valori extreme.

## 4. Analiza corelațiilor Pearson

A fost utilizat coeficientul de corelație Pearson pentru evaluarea asocierilor liniare dintre variabile.

Coeficientul Pearson ia valori între -1 și +1:

- Valori pozitive indică asocieri liniare directe.
- Valori negative indică asocieri liniare inverse.
- Valori apropiate de zero indică asocieri liniare slabe.

### Corelații globale

| Relație | Coeficient Pearson aproximativ |
|---|---:|
| Suprafață – temperatura aerului | -0,02 |
| Suprafață – precipitații | -0,10 |
| Suprafață – MODIS zi | -0,07 |
| Suprafață – MODIS noapte | +0,02 |
| Temperatura aerului – MODIS zi | +0,93 |
| Temperatura aerului – MODIS noapte | +0,97 |
| MODIS zi – MODIS noapte | +0,91 |

Rezultatele indică asocieri globale slabe între suprafața apei și factorii meteorologici, dar asocieri puternice între variabilele de temperatură.

## 5. Corelații individuale pe lac

Pentru a evita interpretarea exclusivă a rezultatelor agregate, au fost calculate corelații separate pentru fiecare lac.

| Lac | Suprafață–temperatură aer | Suprafață–precipitații | Suprafață–MODIS zi | Suprafață–MODIS noapte |
|---|---:|---:|---:|---:|
| Amara | -0,72 | -0,15 | -0,54 | -0,70 |
| Nuntași | -0,20 | +0,25 | -0,31 | -0,14 |
| Techirghiol | +0,17 | 0,00 | +0,24 | +0,20 |

**Amara:** prezintă o asociere negativă mai puternică între suprafața apei și temperatură.

**Nuntași:** prezintă asocieri mai slabe, inclusiv o asociere pozitivă modestă cu precipitațiile.

**Techirghiol:** prezintă asocieri slabe, predominant pozitive, între suprafața apei și temperaturi.

Diferențele dintre lacuri justifică analiza individuală a seriilor temporale în etapa următoare.

## 6. Acoperirea temporală

Fișierul `CP2_acoperire_pe_lac.csv` documentează disponibilitatea observațiilor pentru fiecare lac.

Din cele 252 combinații posibile lac × lună pentru perioada 2015–2021, au fost păstrate 139 observații valide.

Selecția a utilizat un prag minim de acoperire JRC de 90%.

## 7. Fișiere disponibile

**Tabele CSV:**

- `CP2_acoperire_pe_lac.csv` – acoperirea observațiilor pentru fiecare lac.
- `CP2_corelatii_Amara.csv` – corelații pentru Amara.
- `CP2_corelatii_Nuntasi.csv` – corelații pentru Nuntași.
- `CP2_corelatii_Techirghiol.csv` – corelații pentru Techirghiol.
- `CP2_corelatii_pearson_original.csv` – corelațiile globale calculate pe variabilele în unitățile originale.
- `CP2_corelatii_train_standardizat.csv` – corelațiile variabilelor standardizate din setul train.
- `CP2_statistici_descriptive.csv` – indicatorii statistici descriptivi.

**Reprezentări grafice:**

- Cinci histograme ale distribuțiilor.
- `CP2_harta_corelatii.png` – matricea globală de corelații.
- `CP2_harta_corelatii_Amara.png` – matricea pentru Amara.
- `CP2_harta_corelatii_Nuntasi.png` – matricea pentru Nuntași.
- `CP2_harta_corelatii_Techirghiol.png` – matricea pentru Techirghiol.

## 8. Interpretare și limitări

Corelațiile Pearson evidențiază asocieri liniare, dar nu demonstrează cauzalitatea.

Interpretarea rezultatelor trebuie să țină cont de:

- Sezonalitatea temperaturilor și a suprafeței apei.
- Diferențele dintre caracteristicile lacurilor.
- Acoperirea temporală incompletă.
- Posibile relații întârziate între precipitații și variațiile suprafeței lacurilor.

Corelațiile globale pot masca relații specifice fiecărui lac.

## 9. Reproducibilitate

Analiza a fost generată folosind scriptul `CP2_U7_analiza_corelatii.py`, disponibil în folderul principal `CP2_U7`.

Datele utilizate provin din integrarea CP1 și din etapa de preprocesare CP2.

## 10. Concluzii

Analiza evidențiază o corelație puternică între variabilele de temperatură ERA5-Land și MODIS, dar relații diferite între factorii meteorologici și suprafața apei pentru cele trei lacuri.

Rezultatele justifică aprofundarea analizei temporale și investigarea separată a fiecărui lac în etapa CP3.
