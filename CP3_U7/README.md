# CP3 – Reducerea dimensionalității: PCA și t-SNE

**Student:** Andronic Elena Denisa  
**Disciplina:** Metode de explorare a datelor eterogene  
**Unitate:** U7  
**Perioada:** 2015–2021

## Descriere

Etapa CP3 urmărește compararea metodelor de reducere a dimensionalității **PCA (baseline)** și **t-SNE**, utilizând date despre lacurile Techirghiol, Amara și Nuntași.

Analiza folosește trei surse: JRC Global Surface Water, ERA5-Land și MODIS LST, integrate într-o matrice de **139 observații × 5 trăsături**, cu split temporal de 99 observații train și 40 test.

## Metodologie și rezultate

Metodele sunt aplicate pe surse separate și pe datele combinate, fiind evaluate prin varianță explicată, eroare de reconstrucție și trustworthiness.

Pentru datele combinate, **PCA explică 82,34% din varianță** prin primele două componente, iar t-SNE obține un trustworthiness de **0,9892**, comparativ cu **0,9138** pentru PCA.

Stabilitatea t-SNE este verificată folosind trei seed-uri și subperioade temporale.

## Reproducibilitate

Scripturile Python și rezultatele experimentale sunt organizate în folderele `PCA` și `tSNE`, fiecare având documentație separată.

Datele preprocesate provin din etapa CP2.

**Concluzie:** t-SNE păstrează mai bine vecinătățile locale ale datelor combinate, în timp ce PCA oferă o reprezentare liniară interpretabilă.
