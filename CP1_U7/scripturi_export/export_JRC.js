
/****************************************************
 CP1 - Evolutia suprafetei lacurilor din Romania
 Lacuri: Techirghiol, Amara, Nuntasi
 Perioada: 2015-2021
 Sursa: JRC Global Surface Water
****************************************************/

// ================================================
// 1. TRANSFORMAM CONTURURILE IN POLIGOANE
// ================================================

function transformaInPoligon(colectie) {

  var contur = ee.FeatureCollection(colectie)
    .first()
    .geometry();

  return ee.Geometry.Polygon([
    contur.coordinates()
  ]);
}

var techirghiol = transformaInPoligon(
  zona_techirghiol
);

var amara = transformaInPoligon(
  zona_amara
);

var nuntasi = transformaInPoligon(
  zona_nuntasi
);

// ================================================
// 2. VERIFICAM SUPRAFETELE POLIGOANELOR
// ================================================

print(
  'Suprafata zonei Techirghiol (km2):',
  techirghiol.area(1).divide(1e6)
);

print(
  'Suprafata zonei Amara (km2):',
  amara.area(1).divide(1e6)
);

print(
  'Suprafata zonei Nuntasi (km2):',
  nuntasi.area(1).divide(1e6)
);

// ================================================
// 3. INCARCAM IMAGINILE LUNARE JRC
// ================================================

var jrc = ee.ImageCollection(
  'JRC/GSW1_4/MonthlyHistory'
).filterDate('2015-01-01', '2022-01-01');

print('Numar imagini lunare:', jrc.size());

// 7 ani x 12 luni = 84 luni
var luni = ee.List.sequence(0, 83);

// ================================================
// 4. CALCULAM SUPRAFATA APEI PENTRU UN LAC
// ================================================

function calculeazaLac(numeLac, geometrie) {

  var observatii = luni.map(function(index) {

    var data = ee.Date('2015-01-01')
      .advance(index, 'month');

    var imagine = ee.Image(
      jrc.filterDate(
        data,
        data.advance(1, 'month')
      ).first()
    );

    // JRC water:
    // 0 = fara date
    // 1 = teren
    // 2 = apa
    var bandaApa = imagine.select('water');

    // Suprafata acoperita de apa
    var imagineArieApa = ee.Image.pixelArea()
      .updateMask(bandaApa.eq(2))
      .rename('arie_apa');

    var rezultatApa = imagineArieApa.reduceRegion({
      reducer: ee.Reducer.sum(),
      geometry: geometrie,
      scale: 30,
      maxPixels: 1e9,
      tileScale: 4
    });

    var arieApaM2 = ee.Number(
      ee.Algorithms.If(
        ee.Algorithms.IsEqual(
          rezultatApa.get('arie_apa'), null
        ),
        0,
        rezultatApa.get('arie_apa')
      )
    );

    // Suprafata cu date valide
    var imagineArieValida = ee.Image.pixelArea()
      .updateMask(bandaApa.eq(1).or(bandaApa.eq(2)))
      .rename('arie_valida');

    var rezultatValid = imagineArieValida.reduceRegion({
      reducer: ee.Reducer.sum(),
      geometry: geometrie,
      scale: 30,
      maxPixels: 1e9,
      tileScale: 4
    });

    var arieValidaM2 = ee.Number(
      ee.Algorithms.If(
        ee.Algorithms.IsEqual(
          rezultatValid.get('arie_valida'), null
        ),
        0,
        rezultatValid.get('arie_valida')
      )
    );

    var arieZonaM2 = geometrie.area(1);

    var acoperirePct = arieValidaM2
      .divide(arieZonaM2)
      .multiply(100);

    // Daca nu exista observatii valide,
    // suprafata apei ramane null, nu zero
    var suprafataKm2 = ee.Algorithms.If(
      arieValidaM2.gt(0),
      arieApaM2.divide(1e6),
      null
    );

    return ee.Feature(null, {
      lac: numeLac,
      data: data.format('YYYY-MM'),
      an: data.get('year'),
      luna: data.get('month'),
      suprafata_km2: suprafataKm2,
      arie_valida_km2: arieValidaM2.divide(1e6),
      acoperire_date_pct: acoperirePct,
      arie_zona_km2: arieZonaM2.divide(1e6)
    });

  });

  return ee.FeatureCollection(observatii);
}

// ================================================
// 5. PROCESAM CELE TREI LACURI
// ================================================

var rezultateTechirghiol = calculeazaLac(
  'Techirghiol',
  techirghiol
);

var rezultateAmara = calculeazaLac(
  'Amara',
  amara
);

var rezultateNuntasi = calculeazaLac(
  'Nuntasi',
  nuntasi
);

// ================================================
// 6. COMBINAM REZULTATELE
// ================================================

var rezultate = rezultateTechirghiol
  .merge(rezultateAmara)
  .merge(rezultateNuntasi);

print(
  'Numar total de observatii:',
  rezultate.size()
);

print(
  'Primele 10 observatii:',
  rezultate.limit(10)
);

// ================================================
// 7. AFISAM POLIGOANELE PE HARTA
// ================================================

Map.addLayer(
  techirghiol,
  {color: 'yellow'},
  'Poligon Techirghiol'
);

Map.addLayer(
  amara,
  {color: 'green'},
  'Poligon Amara'
);

Map.addLayer(
  nuntasi,
  {color: 'red'},
  'Poligon Nuntasi'
);

Map.setCenter(28, 44.4, 8);

// ================================================
// 8. EXPORTAM DATELE IN CSV
// ================================================

Export.table.toDrive({
  collection: rezultate,
  description: 'CP1_JRC_Lacuri_2015_2021',
  fileNamePrefix: 'CP1_JRC_Lacuri_2015_2021',
  fileFormat: 'CSV',
  selectors: [
    'lac',
    'data',
    'an',
    'luna',
    'suprafata_km2',
    'arie_valida_km2',
    'acoperire_date_pct',
    'arie_zona_km2'
  ]
});
