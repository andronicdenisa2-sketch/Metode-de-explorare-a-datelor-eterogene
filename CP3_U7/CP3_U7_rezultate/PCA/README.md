# CP3 – Analiza PCA (Baseline)

## Descriere

În această etapă, metoda **Principal Component Analysis (PCA)** este utilizată ca baseline pentru reducerea dimensionalității datelor provenite din JRC Global Surface Water, ERA5-Land și MODIS LST.

Analiza este realizată separat pentru fiecare sursă și pentru datele combinate, utilizând **139 observații lac × lună**, dintre care 99 pentru antrenare și 40 pentru testare.

## Metodologie

PCA este aplicată asupra datelor standardizate în CP2, folosind exclusiv setul de antrenare pentru ajustarea modelului.

Sunt evaluate varianța explicată, contribuțiile componentelor principale și eroarea de reconstrucție (RMSE) pe train și test.

## Rezultate

| Sursă | Varianță explicată de PC1 |
|---|---:|
| JRC | 100,00% |
| ERA5-Land | 57,08% |
| MODIS | 94,83% |
| Date combinate | 57,64% |

Pentru datele combinate, primele două componente explică **82,34% din varianța totală a setului de antrenare**.

JRC conține o singură trăsătură, astfel încât PCA păstrează automat 100% din varianță. Pentru ERA5-Land și MODIS, utilizarea ambelor componente păstrează integral cele două dimensiuni inițiale.

## Fișiere și reproducibilitate

Folderul conține tabele CSV cu varianța explicată, coeficienții componentelor și erorile de reconstrucție, precum și graficele PCA pentru fiecare grup de date.

Rezultatele sunt generate de scriptul `CP3_U7_PCA_baseline.py`, disponibil în folderul principal `CP3_U7`, folosind matricea standardizată din CP2.

## Concluzie

PCA evidențiază o redundanță ridicată între variabilele MODIS și permite sintetizarea celor cinci trăsături combinate în două componente care păstrează **82,34% din varianță**.

Rezultatele constituie baseline-ul pentru comparația cu metoda neliniară t-SNE.
