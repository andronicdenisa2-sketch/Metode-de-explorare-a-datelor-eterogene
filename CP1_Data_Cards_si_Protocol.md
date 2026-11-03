# CP1 — Fișe de date, protocol de aliniere și matricea X

**Tema:** Analiza evoluției suprafeței lacurilor din România în raport cu factorii meteorologici  
**Unitate de observație:** lac × lună  
**Lacuri:** Techirghiol (Constanța), Amara (Ialomița), Nuntași (Constanța)  
**Perioada efectivă a setului integrat:** ianuarie 2015 – decembrie 2021 (84 luni × 3 lacuri = 252 rânduri)

## 1. Fișa sursei — JRC Global Surface Water

- **Produs folosit:** `JRC/GSW1_4/MonthlyHistory`, Google Earth Engine.
- **Rol:** estimarea lunară a suprafeței ocupate de apă (variabila de interes) și a acoperirii observațiilor.
- **Acoperire istorică a produsului:** 1984–2021; subset extras: 2015–2021.
- **Rezoluție:** 30 m; observații lunare.
- **Geografie:** trei poligoane de studiu desenate manual, transformate din contururi `LinearRing` în poligoane.
- **Prelucrare:** clasa `water = 2` considerată apă; `water = 1` teren; `water = 0` fără date. Se însumează aria pixelilor de apă, exprimată în km². Acoperirea datelor este calculată separat.
- **Variabile:** `suprafata_km2`, `arie_valida_km2`, `acoperire_date_pct`, `arie_zona_km2`.
- **Lipsuri / QC:** 90 luni fără valoare de suprafață; în total 113 luni nu îndeplinesc regula „suprafață disponibilă și acoperire ≥90%”. 139 luni sunt admise pentru analiza principală.
- **Limitări:** norii și lipsa observațiilor; posibilă confuzie între apă și teren; suprafața observată este constrânsă de conturul ales. Lipsa datelor nu înseamnă apă absentă.
- **Fișier:** `CP1_JRC_Lacuri_2015_2021.csv`.

## 2. Fișa sursei — Copernicus ERA5-Land

- **Produs folosit:** `ECMWF/ERA5_LAND/MONTHLY_AGGR`, Google Earth Engine.
- **Rol:** descrierea condițiilor meteorologice care ar putea fi asociate cu modificările suprafeței lacurilor.
- **Subset extras:** 2015–2021, lunar.
- **Rezoluție spațială:** aproximativ 11 km; valori extrase la centroidul fiecărui lac, nu măsurate direct în apă.
- **Prelucrare:** `temperature_2m` în Kelvin → °C prin scăderea a 273,15; `total_precipitation_sum` în metri → mm prin înmulțirea cu 1000.
- **Variabile:** `temperatura_medie_c`, `precipitatii_totale_mm`.
- **Lipsuri / QC:** niciuna în cele 252 rânduri exportate.
- **Limitări:** reanaliză meteorologică, nu observații directe din stații; rezoluție grosieră; temperatura aerului diferă de temperatura suprafeței.
- **Fișier:** `CP1_ERA5_Lacuri_2015_2021.csv`.

## 3. Fișa sursei — MODIS LST

- **Produs folosit:** `MODIS/061/MOD11A2`, Terra, Google Earth Engine.
- **Rol:** indicator termic suplimentar, comparat cu informațiile optice și meteorologice.
- **Subset extras:** 2015–2021; 322 compozite de aproximativ 8 zile, agregate în medii lunare.
- **Rezoluție:** aproximativ 1 km.
- **Prelucrare:** benzile `LST_Day_1km` și `LST_Night_1km`, factor 0,02, conversie Kelvin → °C; filtrare QC pe biții de calitate 0–1; media lunară a imaginilor și media spațială în fiecare poligon.
- **Variabile:** `lst_zi_c`, `lst_noapte_c`, `numar_imagini_modis`.
- **Lipsuri / QC:** 15 valori lipsă pentru LST noapte în setul complet; 13 în subsetul JRC valid (139 rânduri).
- **Limitări:** LST este temperatura radiometrică a suprafeței, nu temperatura apei măsurată in situ; pixeli de 1 km pot amesteca apă și uscat, mai ales la lacuri mici; calitatea variază cu condițiile de observație.
- **Fișier:** `CP1_MODIS_LST_2015_2021.csv`.

## 4. Aliniere și verificare

1. **Spațial:** trei regiuni de interes constante; JRC calculat în poligoane, ERA5 la centroid, MODIS agregat în poligoane. Rezoluțiile originale nu sunt identice și nu pretindem că au fost reproiectate la o rezoluție fizică comună.
2. **Temporal:** lună calendaristică `YYYY-MM`; MODIS (8 zile) agregat la medie lunară; JRC și ERA5 sunt deja lunare.
3. **Semantic:** chei `lac` și `data`; suprafață km², temperaturi °C, precipitații mm.
4. **Join:** verificare a unicității cheii și a coincidenței celor 252 chei între surse.
5. **QC:** observațiile JRC fără suprafață sau cu acoperire sub 90% nu intră în subsetul principal; variațiile consecutive de peste 30% sunt marcate, nu eliminate automat.
6. **Rezultat:** 252 rânduri brute; 139 rânduri selectate (Techirghiol 45, Amara 51, Nuntași 43); 6 variații marcate, toate la Nuntași.

## 5. Pipeline care produce X

**Script executabil:** `pipeline_cp1_X.py` (Python standard library, fără dependențe externe). Se rulează cu cele trei fișiere CSV în același director:

```bash
python pipeline_cp1_X.py
```

**Ieșiri:**

- `CP1_Date_QC_pipeline.csv`: 252 rânduri și indicatorii de calitate.
- `CP1_X_optic_2015_2021.csv`: 139 rânduri × 1 caracteristică (`suprafata_km2`), plus cheile de identificare.
- `CP1_X_integrat_2015_2021.csv`: 139 rânduri × 5 caracteristici (`suprafata_km2`, `temperatura_medie_c`, `precipitatii_totale_mm`, `lst_zi_c`, `lst_noapte_c`), plus cheile. Există 13 valori lipsă la `lst_noapte_c`.

**Scalare corectă:** în CP1 valorile sunt păstrate în unități fizice. La CP2 se va defini un split temporal și se va ajusta scalerul exclusiv pe antrenare; aceiași parametri vor fi aplicați validării/testului. Imputarea valorilor lipsă se va ajusta tot exclusiv pe antrenare.

**Atenție la definirea țintei:** pentru PCA descriptivă, suprafața JRC poate fi o caracteristică în X. Dar dacă sarcina ulterioară este **predicția suprafeței lacului**, suprafața JRC din aceeași lună nu poate fi folosită ca predictor al aceleiași suprafețe: aceasta ar fi scurgere directă a țintei (*target leakage*). Pentru predicție se definește `y = suprafata_km2` la luna țintă și se folosesc predictori disponibili anterior (de exemplu suprafața la t−1, meteo la t−1, LST la t−1), cu split temporal. Comparația optic vs. integrat trebuie păstrată în același protocol.

## 6. Blocaje și următorii pași

- **2022–2025:** necesită o sursă optică suplimentară, precum Sentinel-2/Landsat; nu este acoperită de JRC MonthlyHistory.
- **Agregare la 10 zile:** nu poate fi derivată fidel din JRC MonthlyHistory; necesită observații optice mai frecvente.
- **Date lipsă:** 13 valori MODIS noapte în subsetul selectat; strategie de imputare de stabilit în protocolul CP2.
- **Validarea schimbărilor extreme:** comparație cu observații independente și cu literatura despre Nuntași–Tuzla.
- **Literatură:** cele două articole-ancoră din CP0 trebuie completate până la un tabel SOA de 10 lucrări verificate bibliografic.

## 7. Legătura cu întrebarea de cercetare

Întrebarea CP0: „În ce măsură variațiile precipitațiilor și temperaturilor explică reducerea suprafeței unor lacuri din România în ultimii ani?”

Setul integrat permite explorarea asocierilor și pregătirea unui protocol comparativ; **nu demonstrează încă o explicație cauzală**. Intervențiile umane și alți factori hidrologici pot influența suprafața lacurilor.
