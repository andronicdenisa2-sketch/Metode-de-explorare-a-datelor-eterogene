# SOA — Evoluția suprafeței lacurilor din România și factorii meteorologici (U7)

Document SOA pentru CP1 (aliniere spațială, temporală și semantică; acoperire și valori lipsă). Stadiul actual pentru proiectul **„Analiza evoluției suprafeței lacurilor din România în raport cu factorii meteorologici”**. Întrebarea de cercetare: *În ce măsură variațiile precipitațiilor și temperaturilor explică reducerea suprafeței unor lacuri din România în ultimii ani?*

Sunt analizate **10 articole științifice**, inclusiv cele două studii despre **Nuntași–Tuzla** din CP0. Tabelul sintetizează referința bibliografică, sursele de date, metoda, metrica și rezultatul fiecărui studiu. Linkurile duc la **pagina articolului la editor sau într-un depozit academic**, nu exclusiv la doi.org. Lucrările metodologice sunt descrise calitativ când nu există o cifră comparabilă.

|#|Referință|Surse de date|Metodă de explorare|Metrică|Rezultat (cifra principală / constatarea din articol)|
|-|-|-|-|-|-|
|1|*Surface Water Change Detection via Water Indices and Predictive Modeling Using Remote Sensing Imagery: A Case Study of Nuntasi-Tuzla Lake, Romania*. **Water 14(4), 556 (2022)**. URL: https://www.mdpi.com/2073-4441/14/4/556|Imagini satelitare și indici de apă; cazul Nuntași–Tuzla|Analiza multitemporală a suprafeței apei și modelare predictivă; discută clima și intervențiile umane|Suprafața apei și variația sa în timp|Documentează reducerea accentuată a suprafeței lacului în vara anului **2020**; nu atribuim aici un procent neverificat|
|2|**Jitariu, V., Dorosencu, A., Ichim, P., Ion, C.** — *Severe Drought Monitoring by Remote Sensing Methods and Its Impact on Wetlands Birds Assemblages in Nuntași and Tuzla Lakes (Danube Delta Biosphere Reserve)*. **Land 11(5), 672 (2022)**. URL: https://www.mdpi.com/2073-445X/11/5/672|Observații de teledetecție, lacurile Nuntași și Tuzla, informații despre păsări acvatice|Monitorizarea secetei și evaluarea impactului asupra comunităților de păsări|Modificarea suprafețelor umede și indicatori ecologici|Evidențiază episoade de uscare parțială sau totală a lacurilor și consecințe ecologice; nu raportăm o valoare numerică neverificată|
|3|**Pekel, J.-F., Cottam, A., Gorelick, N., Belward, A. S.** — *High-resolution mapping of global surface water and its long-term changes*. **Nature 540, 418–422 (2016)**. URL: https://www.nature.com/articles/nature20584|Peste 3 milioane de imagini Landsat|Cartografierea schimbărilor lunare ale apei de suprafață la 30 m|Suprafață de apă și schimbări în timp|Identifică o scădere a suprafețelor de apă de aproape **90.000 km²** în anumite regiuni, compensată parțial de apariția apei în altele|
|4|**Muñoz-Sabater, J. et al.** — *ERA5-Land: a state-of-the-art global reanalysis dataset for land applications*. **Earth System Science Data 13, 4349–4383 (2021)**. URL: https://essd.copernicus.org/articles/13/4349/2021/|Reanaliză meteorologică ERA5-Land|Descrierea și evaluarea produsului de reanaliză terestră|Calitatea variabilelor meteorologice, consistența spațio-temporală|Fundamentează utilizarea temperaturii aerului și precipitațiilor ca variabile meteorologice; nu este un studiu despre suprafața unui lac anume|
|5|**Wan, Z.** — *New refinements and validation of the collection-6 MODIS land-surface temperature/emissivity product*. **Remote Sensing of Environment 140, 36–45 (2014)**. URL: https://www.sciencedirect.com/science/article/pii/S003442571300285X|MODIS LST și observații de validare|Rafinarea algoritmilor LST și validare radiometrică|Eroare de temperatură, K|În validările discutate, erorile produselor analizate sunt în general în limita **±2 K**, adesea **±1 K**, cu excepții; nu garantează această eroare pentru lacurile noastre|
|6|**Huang, C., Chen, Y., Zhang, S., Wu, J.** — *Detecting, Extracting, and Monitoring Surface Water From Space Using Optical Sensors: A Review*. **Reviews of Geophysics 56, 333–360 (2018)**. URL: https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2018RG000598|Literatură despre senzori optici, Landsat și alte surse satelitare|Revizuire a tehnicilor de identificare și monitorizare a apei|Acuratețe, rezoluție spațială și temporală, acoperire|Evidențiază limitările provocate de nori, vegetație și compromisurile de rezoluție; recomandă integrarea mai multor surse|
|7|**McFeeters, S. K.** — *The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features*. **International Journal of Remote Sensing 17(7), 1425–1432 (1996)**. URL: https://www.tandfonline.com/doi/abs/10.1080/01431169608948714|Benzi spectrale verde și infraroșu apropiat|Introducerea indicelui NDWI pentru delimitarea apei|Separabilitatea apei față de teren|Propune NDWI ca metodă de evidențiere a corpurilor de apă; articol metodologic, fără o singură cifră de performanță transferabilă|
|8|**Xu, H.** — *Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery*. **International Journal of Remote Sensing 27(14), 3025–3033 (2006)**. URL: https://www.tandfonline.com/doi/full/10.1080/01431160600589179|Imagini Landsat, benzi verde și infraroșu cu unde scurte|MNDWI: înlocuiește NIR cu SWIR în indicele de apă|Separarea apei de suprafețele construite și vegetație|MNDWI reduce confuziile cu terenul construit și poate îmbunătăți extragerea apei față de NDWI în scene adecvate|
|9|**Yao, F. et al.** — *Satellites reveal widespread decline in global lake water storage*. **Science 380(6646), 743–749 (2023)**. URL: https://pubmed.ncbi.nlm.nih.gov/37200445/|Observații satelitare ale lacurilor la scară globală|Estimarea schimbărilor de stocare a apei și investigarea factorilor asociați|Modificarea volumului / stocării apei|Identifică declinul larg răspândit al rezervelor de apă lacustră; **volumul** nu trebuie confundat cu **suprafața** calculată în U7|
|10|**O'Reilly, C. M. et al.** — *Rapid and highly variable warming of lake surface waters around the globe*. **Geophysical Research Letters 42, 10773–10781 (2015)**. URL: https://agupubs.onlinelibrary.wiley.com/doi/10.1002/2015GL066235|Măsurători in situ și observații satelitare ale temperaturii lacurilor|Sinteză globală a tendințelor temperaturii apei|°C pe deceniu|Temperatura apei de suprafață în timpul verii a crescut în medie cu **0,34 °C/deceniu** în perioada 1985–2009|

## Ce preiau din fiecare articol pentru U7

1. **Nuntași–Tuzla, Water 2022:** precedentul local direct pentru variația suprafeței apei și pentru verificarea scăderilor extreme din seria JRC.
2. **Jitariu et al., Land 2022:** confirmă relevanța secetei și a impactului ecologic; motivează păstrarea observațiilor extreme credibile, nu ștergerea lor automată.
3. **Pekel et al., 2016:** justifică alegerea **JRC Global Surface Water MonthlyHistory** ca sursă pentru variabila de suprafață (km²).
4. **Muñoz-Sabater et al., 2021:** justifică folosirea **ERA5-Land** pentru temperatura aerului (°C) și precipitații (mm).
5. **Wan, 2014:** oferă fundamentul pentru **MODIS LST** și pentru controlul calității; temperatura radiometrică a suprafeței nu este echivalentă cu temperatura apei măsurată direct.
6. **Huang et al., 2018:** susține raportarea acoperirii satelitare și tratarea explicită a observațiilor lipsă; explică avantajul integrării surselor.
7. **McFeeters, 1996:** indicele **NDWI** este un posibil baseline pentru extinderea cu Sentinel-2/Landsat în 2022–2025.
8. **Xu, 2006:** **MNDWI** poate fi comparat cu NDWI în extinderea optică, mai ales în zone cu confuzii între apă și teren.
9. **Yao et al., 2023:** oferă contextul global al reducerii rezervelor de apă, dar ne obligă să distingem între **suprafață** și **volum**.
10. **O'Reilly et al., 2015:** arată relevanța informației termice și variația spațială a încălzirii lacurilor; nu permite deducerea directă a unei relații cauzale cu suprafața.

## Raportarea la cerințele CP1 și la întrebarea Q7.3

* **Unitatea spațio-temporală:** lac × lună (Techirghiol, Amara, Nuntași). Pentru comparații valide trebuie folosite aceleași chei (`lac`, `YYYY-MM`) și unități (km², °C, mm).
* **Aliniere spațială:** JRC este agregat pe conturul fiecărui lac; ERA5-Land este eșantionat în centrul lacului; MODIS este agregat pe zona lacului. Aceste operații au suporturi spațiale diferite, ceea ce limitează interpretarea cauzală.
* **Aliniere temporală:** observațiile JRC sunt lunare, datele ERA5-Land sunt lunare, iar compozitele MODIS de 8 zile sunt agregate lunar. Pentru analiza decalajelor meteorologice trebuie testate ulterior laguri de 1–3 luni și ferestre cumulative de precipitații, fără folosirea informațiilor din viitor.
* **Goluri și calitate:** păstrăm lipsurile ca lipsuri, nu ca suprafață zero; raportăm procentul de acoperire JRC și verificăm separat variațiile bruște. Imputarea, dacă devine necesară, trebuie justificată și evaluată fără scurgeri de informație.
* **Comparația obligatorie U7:** optic singur versus optic + termic + meteo; agregare lunară versus decadală (intervale de aproximativ 10 zile). Comparația decadală **nu este încă realizată**: necesită observații Sentinel-2/Landsat sau alte produse cu frecvență adecvată, nu doar JRC MonthlyHistory.
* **Întrebarea Q7.3:** pentru a identifica lacurile cu reducere persistentă trebuie estimate tendințe pe observațiile de calitate și verificat dacă precipitațiile/temperatura explică o parte din variație; literatura indică și factori antropici, în special pentru Nuntași–Tuzla.

## Note de verificare și limitări





Literatura selectată include atât studii aplicate privind dinamica suprafețelor lacustre, cu accent pe zona Nuntași–Tuzla, cât și lucrări metodologice dedicate teledetecției, identificării suprafețelor acvatice și analizei factorilor climatici.



Metodele și rezultatele prezentate diferă în funcție de rezoluția spațială și temporală, sursele de date utilizate și indicatorii analizați. În consecință, rezultatele studiilor nu sunt întotdeauna direct comparabile.



Lucrările privind temperatura lacurilor și variațiile rezervelor de apă oferă un context complementar analizei suprafeței lacustre. Acestea contribuie la formularea ipotezelor de cercetare, fără a demonstra individual o relație cauzală între factorii meteorologici și reducerea suprafeței apei.



Pentru proiectul U7, literatura analizată fundamentează utilizarea integrată a observațiilor optice, termice și meteorologice, precum și necesitatea evaluării calității și acoperirii datelor.

