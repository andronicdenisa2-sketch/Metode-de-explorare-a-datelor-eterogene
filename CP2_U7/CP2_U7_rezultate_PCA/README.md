# CP2 – Rezultatele analizei PCA

## 1. Obiectiv

Analiza componentelor principale (Principal Component Analysis – PCA) a fost utilizată pentru explorarea structurii datelor și identificarea principalelor direcții de variație ale trăsăturilor provenite din JRC Global Surface Water, ERA5-Land și MODIS LST.

Analiza a fost realizată pentru lacurile Techirghiol, Amara și Nuntași, în perioada 2015–2021.

## 2. Date utilizate

Matricea de intrare conține 139 observații lac × lună și 5 trăsături numerice:

- Suprafața apei (JRC), km².
- Temperatura aerului (ERA5-Land), °C.
- Precipitații lunare (ERA5-Land), mm.
- Temperatura suprafeței terestre în timpul zilei (MODIS LST), °C.
- Temperatura suprafeței terestre în timpul nopții (MODIS LST), °C.

Datele au fost standardizate cu `StandardScaler`, ajustat exclusiv pe setul de antrenare.

Split-ul temporal conține 99 observații train și 40 observații test. PCA a fost ajustată numai pe datele train.

## 3. Varianța explicată

| Componentă | Varianță explicată |
|---|---:|
| PC1 | 57,64% |
| PC2 | 24,70% |
| PC3 | 14,75% |
| PC4 | 1,94% |
| PC5 | 0,97% |
| **PC1 + PC2** | **82,34%** |
| **PC1 + PC2 + PC3** | **97,09%** |

Primele două componente surprind 82,34% din varianța totală a trăsăturilor din setul de antrenare.

## 4. Interpretarea componentelor

**PC1 – Componenta asociată temperaturilor**

PC1 explică aproximativ 57,64% din varianță și este dominată de:

- Temperatura aerului ERA5-Land: 33,14%.
- Temperatura MODIS zi: 32,94%.
- Temperatura MODIS noapte: 31,84%.

Această componentă reflectă variațiile comune ale variabilelor de temperatură.

**PC2 – Componenta asociată suprafeței apei și precipitațiilor**

PC2 explică aproximativ 24,70% din varianță, având contribuțiile principale:

- Suprafața apei JRC: 53,41%.
- Precipitațiile ERA5-Land: 45,37%.

Această componentă surprinde o direcție de variație distinctă de cea dominantă a temperaturilor.

Contribuțiile PCA nu demonstrează o relație cauzală între variabile.

## 5. Evaluarea reconstrucției

A fost evaluată eroarea de reconstrucție pentru diferite numere de componente principale, exprimată prin RMSE în unități standardizate.

| Număr componente | RMSE train | RMSE test |
|---|---:|---:|
| 2 | 0,420 | 0,708 |
| 3 | 0,171 | 0,231 |

Utilizarea a trei componente reduce eroarea de reconstrucție comparativ cu utilizarea a două componente.

## 6. Fișiere disponibile

| Fișier | Conținut |
|---|---|
| `CP2_PCA_coeficienti_componente.csv` | Coeficienții componentelor principale |
| `CP2_PCA_contributii.png` | Graficul contribuțiilor trăsăturilor la PC1 și PC2 |
| `CP2_PCA_contributii_pct.csv` | Contribuțiile procentuale ale trăsăturilor |
| `CP2_PCA_eroare_reconstructie.csv` | Erorile de reconstrucție train/test |
| `CP2_PCA_proiectie_PC1_PC2.png` | Reprezentarea observațiilor în planul PC1–PC2 |
| `CP2_PCA_proiectie_lac_luna.csv` | Coordonatele observațiilor în spațiul PCA |
| `CP2_PCA_varianta_explicata.csv` | Varianța explicată de fiecare componentă |
| `CP2_PCA_varianta_explicata.png` | Graficul varianței explicate |

## 7. Concluzii

Analiza PCA evidențiază două direcții principale de variație: una asociată temperaturilor și alta asociată suprafeței apei și precipitațiilor.

Primele două componente explică 82,34% din varianța datelor de antrenare, iar primele trei explică aproximativ 97,09%.

Rezultatele susțin utilitatea PCA pentru explorarea structurii datelor integrate, dar nu stabilesc cauzele modificării suprafeței lacurilor.

## 8. Reproducibilitate

Rezultatele au fost generate prin scriptul `CP2_U7_analiza_PCA.py`, disponibil în folderul principal `CP2_U7`.

Datele de intrare sunt disponibile în `CP2_U7_date_preprocesate/CP2_X_standardizat.csv`.
