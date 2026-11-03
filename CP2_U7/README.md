# CP2 – Aliniere și trăsături

**Disciplina:** Metode de explorare a datelor eterogene (MEDE)  
**Student:** Andronic Elena Denisa  
**Unitate:** U7  
**Proiect:** Analiza evoluției suprafeței lacurilor din România în raport cu factorii meteorologici

## 1. Obiectivul proiectului

Proiectul urmărește analiza relației dintre variațiile suprafeței unor lacuri din România și factorii meteorologici, în special temperatura și precipitațiile.

**Întrebarea de cercetare:** În ce măsură variațiile precipitațiilor și temperaturilor explică reducerea suprafeței unor lacuri din România în ultimii ani?

Lacurile analizate sunt Techirghiol, Amara și Nuntași, pentru perioada 2015–2021.

## 2. Sursele de date

Au fost integrate trei surse de date eterogene:

| Sursă | Variabile | Caracteristici |
|---|---|---|
| JRC Global Surface Water v1.4 | Suprafața apei (km²) | Istoricul lunar al prezenței apei |
| ERA5-Land Monthly | Temperatura aerului (°C), precipitații (mm) | Date meteorologice lunare |
| MODIS MOD11A2 v6.1 | Temperatura suprafeței terestre, zi/noapte (°C) | Observații satelitare agregate lunar |

Datele au fost extrase și prelucrate inițial prin Google Earth Engine în etapa CP1.

## 3. Alinierea spațială și temporală

Unitatea comună de analiză este **lac × lună**.

Alinierea datelor a urmărit:

- Utilizarea acelorași trei lacuri și a perioadei 2015–2021.
- Calcularea suprafeței apei din observațiile JRC pentru fiecare lac și lună.
- Asocierea temperaturii aerului și precipitațiilor ERA5-Land cu fiecare lac.
- Agregarea observațiilor MODIS LST la nivel lunar.
- Integrarea rezultatelor pe cheia comună formată din identificatorul lacului și lună.

Au fost considerate inițial 252 de combinații posibile (3 lacuri × 84 luni).

După filtrarea observațiilor pe baza disponibilității și acoperirii datelor JRC, au fost păstrate **139 de observații valide**, folosind un prag minim de acoperire de 90%.

Distribuția observațiilor valide:

| Lac | Observații |
|---|---:|
| Amara | 51 |
| Nuntași | 43 |
| Techirghiol | 45 |
| **Total** | **139** |

## 4. Preprocesarea datelor

Preprocesarea a inclus:

1. Verificarea structurii datelor integrate și a valorilor lipsă.
2. Separarea temporală a datelor în antrenare și testare, cu pragul la 1 ianuarie 2020.
3. Tratarea celor 13 valori lipsă ale temperaturii MODIS nocturne prin imputare cu mediana calculată exclusiv pe datele de antrenare.
4. Standardizarea celor cinci variabile numerice folosind `StandardScaler`, ajustat numai pe datele de antrenare.
5. Salvarea matricei standardizate și a rapoartelor de preprocesare.

**Split temporal:**

- Train: 99 observații, din aprilie 2015 până în octombrie 2019.
- Test: 40 observații, din martie 2020 până în septembrie 2021.

Intervalele reprezintă limitele temporale ale observațiilor disponibile, nu serii lunare complete.

## 5. Matricea finală de trăsături

Matricea finală conține **139 observații × 5 trăsături numerice**.

| Trăsătură | Sursă |
|---|---|
| Suprafața apei (km²) | JRC |
| Temperatura aerului (°C) | ERA5-Land |
| Precipitații lunare (mm) | ERA5-Land |
| Temperatura suprafeței – zi (°C) | MODIS |
| Temperatura suprafeței – noapte (°C) | MODIS |

Identificatorul lacului și luna sunt păstrate pentru identificarea observațiilor.

## 6. Analiza exploratorie și corelațiile

Au fost analizate distribuțiile variabilelor și corelațiile Pearson la nivel global și individual pentru fiecare lac.

Rezultatele evidențiază:

- Corelații puternice între temperatura aerului ERA5-Land și temperaturile MODIS, de aproximativ 0,93–0,97.
- Corelații globale slabe între suprafața apei și variabilele meteorologice.
- Relații diferite între suprafața apei și temperatură în funcție de lac.

Aceste corelații descriu asocieri statistice și nu demonstrează relații cauzale.

## 7. Analiza PCA

A fost aplicată analiza componentelor principale (PCA) asupra celor cinci trăsături standardizate.

Modelul PCA a fost ajustat folosind exclusiv setul de antrenare.

| Componentă | Varianță explicată |
|---|---:|
| PC1 | 57,64% |
| PC2 | 24,70% |
| PC3 | 14,75% |
| PC4 | 1,94% |
| PC5 | 0,97% |

**Primele două componente explică împreună 82,34% din varianța datelor de antrenare.**

Interpretarea contribuțiilor:

- PC1 este dominată de temperaturile ERA5-Land și MODIS.
- PC2 este asociată în principal cu suprafața apei și precipitațiile.

PCA este utilizată pentru explorarea structurii datelor, nu pentru demonstrarea cauzelor reducerii suprafeței lacurilor.

## 8. Structura repository-ului

Folderul `CP2_U7` conține:

**Scripturi Python:**
- `CP2_U7_preprocesare_date.py` – preprocesarea, imputarea și standardizarea.
- `CP2_U7_analiza_corelatii.py` – distribuții și corelații Pearson.
- `CP2_U7_analiza_PCA.py` – analiza componentelor principale.

**Foldere de rezultate:**
- `CP2_U7_date_preprocesate/` – matricea standardizată, raportul de preprocesare și split-ul temporal.
- `CP2_U7_rezultate_corelatii/` – tabelele și graficele corelațiilor.
- `CP2_U7_rezultate_PCA/` – rezultatele și reprezentările grafice PCA.

**Imagini suplimentare:** capturi ale rulării scripturilor și ale rezultatelor obținute.

## 9. Reproducibilitate

Analizele au fost realizate în Python, utilizând biblioteci precum `pandas`, `numpy`, `matplotlib`, `seaborn` și `scikit-learn`.

Scripturile se execută în următoarea ordine:

1. `CP2_U7_preprocesare_date.py`
2. `CP2_U7_analiza_corelatii.py`
3. `CP2_U7_analiza_PCA.py`

Pentru reproducerea completă este necesar și fișierul integrat din CP1, `CP1_X_integrat_2015_2021.csv`.

## 10. Limitări și pașii următori

Principalele limitări sunt acoperirea temporală incompletă a observațiilor JRC, diferențele de rezoluție dintre sursele de date și dificultatea separării sezonalității de tendințele pe termen lung.

În etapa CP3 sunt planificate:

- Analiza evoluției lunare a suprafeței fiecărui lac.
- Investigarea sezonalității și a tendințelor temporale.
- Analiza corelațiilor cu decalaje temporale.
- Comparația cantitativă dintre analiza bazată pe o singură sursă și cea bazată pe integrarea surselor.

Comparația cantitativă baseline versus surse combinate nu a fost încă realizată în CP2.
