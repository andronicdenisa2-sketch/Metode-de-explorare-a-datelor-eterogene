# CP3 – Analiza t-SNE

## Descriere

Metoda **t-distributed Stochastic Neighbor Embedding (t-SNE)** este utilizată pentru reducerea neliniară a dimensionalității și vizualizarea relațiilor dintre observațiile lacurilor Techirghiol, Amara și Nuntași.

Analiza este realizată separat pentru ERA5-Land și MODIS, precum și pentru datele combinate, folosind **99 observații din setul de antrenare**.

JRC nu este inclus în comparația bidimensională, deoarece conține o singură trăsătură.

## Metodologie

t-SNE este aplicată asupra datelor standardizate în CP2, cu proiecție în două dimensiuni.

Evaluarea utilizează metrica **trustworthiness (5 vecini)**, care măsoară păstrarea vecinătăților locale.

Stabilitatea rezultatelor este analizată folosind trei seed-uri (42, 123, 2026) și două subperioade temporale: 2015–2017 și 2018–2019.

## Rezultate

| Sursă | PCA – Trustworthiness | t-SNE – Trustworthiness |
|---|---:|---:|
| ERA5-Land | 1,0000 | 0,9962 |
| MODIS | 1,0000 | 0,9949 |
| Date combinate | 0,9138 | 0,9892 |

Valorile t-SNE reprezintă mediile obținute pentru cele trei seed-uri.

Pentru datele combinate, t-SNE păstrează mai bine vecinătățile locale decât PCA în două dimensiuni.

Abaterile standard reduse între rulări indică rezultate consistente din perspectiva metricii evaluate.

## Fișiere și reproducibilitate

Folderul conține fișiere CSV cu metricile comparative PCA–t-SNE și analiza stabilității, precum și graficele bidimensionale pentru fiecare grup de date.

Rezultatele sunt generate de scriptul `CP3_U7_tSNE_stabilitate.py`, disponibil în folderul principal `CP3_U7`, folosind datele standardizate din CP2.

## Concluzie

t-SNE obține un **trustworthiness mediu de 0,9892** pentru datele combinate, comparativ cu **0,9138 pentru PCA**, evidențiind o păstrare mai bună a structurii locale.

Metoda este utilă pentru explorarea vizuală a datelor, fără a demonstra relații cauzale între factorii meteorologici și evoluția suprafeței lacurilor.
