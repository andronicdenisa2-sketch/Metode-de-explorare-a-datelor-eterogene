# CP2 – Date preprocesate

Acest folder conține rezultatele etapei de preprocesare pentru analiza evoluției suprafeței lacurilor Techirghiol, Amara și Nuntași, în perioada 2015–2021.

## Fișiere disponibile

**1. CP2_X_standardizat.csv**

Matricea finală de date, cu 139 de observații lac × lună și 5 trăsături numerice standardizate, provenite din JRC Global Surface Water, ERA5-Land și MODIS LST.

**2. CP2_raport_preprocesare.csv**

Raportul operațiilor de preprocesare, inclusiv tratarea valorilor lipsă și standardizarea variabilelor.

**3. CP2_split_temporal.csv**

Distribuția observațiilor între seturile de antrenare și testare, folosind o separare temporală la 1 ianuarie 2020:
- Train: 99 observații.
- Test: 40 observații.

## Metodologie

Au fost tratate 13 valori lipsă MODIS LST nocturn, folosind mediana calculată exclusiv pe setul de antrenare.

Standardizarea s-a realizat cu `StandardScaler`, ajustat numai pe datele train, pentru a evita scurgerea informațiilor din setul de test.

Rezultatele sunt generate de scriptul `CP2_U7_preprocesare_date.py` din folderul principal `CP2_U7`.
