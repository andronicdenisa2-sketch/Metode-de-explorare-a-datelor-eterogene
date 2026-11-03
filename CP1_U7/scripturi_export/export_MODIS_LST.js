
/****************************************************
 CP1 - TEMPERATURA SUPRAFETEI MODIS LST
 Lacuri: Techirghiol, Amara, Nuntasi
 Perioada: 2015-2021

 Sursa: MODIS Terra MOD11A2 Collection 6.1
 Rezolutie: aproximativ 1 km
 Frecventa: 8 zile

 Rezultate:
 - LST medie zi (C)
 - LST medie noapte (C)
 - numar imagini lunare
****************************************************/

// ================================================
// 1. CONVERTIM CONTURURILE IN POLIGOANE
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
// 2. DEFINIM LACURILE
// ================================================

var lacuri = ee.FeatureCollection([
  ee.Feature(techirghiol, {
    lac: 'Techirghiol'
  }),
  ee.Feature(amara, {
    lac: 'Amara'
  }),
  ee.Feature(nuntasi, {
    lac: 'Nuntasi'
  })
]);

// ================================================
// 3. INCARCAM DATELE MODIS
// ================================================

var modis = ee.ImageCollection(
  'MODIS/061/MOD11A2'
).filterDate('2015-01-01', '2022-01-01');

print('Numar imagini MODIS:', modis.size());

// ================================================
// 4. PRELUCRAM TEMPERATURILE
// ================================================

var modisProcesat = modis.map(function(img) {

  // QC_Day si QC_Night:
  // Pastram pixelii cu calitate obligatorie buna
  // (bitii 0-1 egali cu 00 sau 01).

  var qcZi = img.select('QC_Day')
    .bitwiseAnd(3).lte(1);

  var qcNoapte = img.select('QC_Night')
    .bitwiseAnd(3).lte(1);

  // Factorul de scalare este 0.02.
  // Convertim Kelvin in Celsius.

  var zi = img.select('LST_Day_1km')
    .multiply(0.02)
    .subtract(273.15)
    .updateMask(qcZi)
    .rename('lst_zi_c');

  var noapte = img.select('LST_Night_1km')
    .multiply(0.02)
    .subtract(273.15)
    .updateMask(qcNoapte)
    .rename('lst_noapte_c');

  return zi.addBands(noapte)
    .copyProperties(img, ['system:time_start']);
});

// ================================================
// 5. CALCULAM MEDIILE LUNARE
// ================================================

var luni = ee.List.sequence(0, 83);

var rezultateLista = luni.map(function(index) {

  var data = ee.Date('2015-01-01')
    .advance(index, 'month');

  var imaginiLuna = modisProcesat.filterDate(
    data,
    data.advance(1, 'month')
  );

  var medieLunara = imaginiLuna.mean();

  // Media spatiala in interiorul fiecarui lac
  var statistici = medieLunara.reduceRegions({
    collection: lacuri,
    reducer: ee.Reducer.mean(),
    scale: 1000,
    tileScale: 8
  });

  return statistici.map(function(feature) {

    return ee.Feature(null, {
      lac: feature.get('lac'),
      data: data.format('YYYY-MM'),
      an: data.get('year'),
      luna: data.get('month'),
      lst_zi_c: feature.get('lst_zi_c'),
      lst_noapte_c: feature.get('lst_noapte_c'),
      numar_imagini_modis: imaginiLuna.size()
    });

  });

});

// ================================================
// 6. COMBINAM REZULTATELE
// ================================================

var rezultate = ee.FeatureCollection(
  rezultateLista
).flatten();

print('Numar observatii asteptate:', 252);

// ================================================
// 7. AFISAM LACURILE
// ================================================

Map.addLayer(
  lacuri.style({
    color: 'yellow',
    fillColor: '00000000',
    width: 2
  }),
  {},
  'Lacurile analizate'
);

Map.setCenter(28, 44.4, 8);

// ================================================
// 8. EXPORTAM DATELE IN CSV
// ================================================

Export.table.toDrive({
  collection: rezultate,
  description: 'CP1_MODIS_LST_2015_2021',
  fileNamePrefix: 'CP1_MODIS_LST_2015_2021',
  fileFormat: 'CSV',
  selectors: [
    'lac',
    'data',
    'an',
    'luna',
    'lst_zi_c',
    'lst_noapte_c',
    'numar_imagini_modis'
  ]
});
