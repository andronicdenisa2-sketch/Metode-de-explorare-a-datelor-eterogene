
/****************************************************
 CP1 - DATE METEOROLOGICE ERA5-LAND
 Lacuri: Techirghiol, Amara, Nuntasi
 Perioada: 2015-2021

 Variabile:
 - temperatura medie lunara (C)
 - precipitatii totale lunare (mm)

 Metoda:
 - extragere din punctul interior al fiecarui lac
 - rezolutie ERA5-Land: aproximativ 11 km
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
// 2. DEFINIM PUNCTELE DE EXTRAGERE
// ================================================

// Centroidul fiecarei zone delimitate

var punctTechirghiol = techirghiol.centroid(1);
var punctAmara = amara.centroid(1);
var punctNuntasi = nuntasi.centroid(1);

var puncte = ee.FeatureCollection([
  ee.Feature(punctTechirghiol, {
    lac: 'Techirghiol'
  }),
  ee.Feature(punctAmara, {
    lac: 'Amara'
  }),
  ee.Feature(punctNuntasi, {
    lac: 'Nuntasi'
  })
]);

// ================================================
// 3. INCARCAM DATELE ERA5-LAND
// ================================================

var era5 = ee.ImageCollection(
  'ECMWF/ERA5_LAND/MONTHLY_AGGR'
)
.filterDate('2015-01-01', '2022-01-01')
.select([
  'temperature_2m',
  'total_precipitation_sum'
])
.sort('system:time_start');

print('Numar imagini ERA5-Land:', era5.size());

// ================================================
// 4. CONVERTIM UNITATILE
// ================================================

var era5Procesat = era5.map(function(img) {

  var temperatura = img
    .select('temperature_2m')
    .subtract(273.15)
    .rename('temperatura_medie_c');

  var precipitatii = img
    .select('total_precipitation_sum')
    .multiply(1000)
    .rename('precipitatii_totale_mm');

  return temperatura
    .addBands(precipitatii)
    .copyProperties(img, ['system:time_start']);
});

// ================================================
// 5. EXTRAGEM DATELE PENTRU FIECARE LUNA
// ================================================

var listaImagini = era5Procesat.toList(84);

var luni = ee.List.sequence(0, 83);

var rezultateLista = luni.map(function(index) {

  var imagine = ee.Image(listaImagini.get(index));

  var data = ee.Date(
    imagine.get('system:time_start')
  );

  // Extragem valorile pentru cele 3 puncte
  var valori = imagine.sampleRegions({
    collection: puncte,
    properties: ['lac'],
    scale: 11132,
    geometries: false,
    tileScale: 4
  });

  return valori.map(function(feature) {

    return ee.Feature(null, {
      lac: feature.get('lac'),
      data: data.format('YYYY-MM'),
      an: data.get('year'),
      luna: data.get('month'),
      temperatura_medie_c:
        feature.get('temperatura_medie_c'),
      precipitatii_totale_mm:
        feature.get('precipitatii_totale_mm')
    });

  });
});

// ================================================
// 6. COMBINAM REZULTATELE
// ================================================

var rezultate = ee.FeatureCollection(
  rezultateLista
).flatten();

// Afisam doar numarul asteptat de observatii.
// Nu fortam evaluarea tuturor calculelor.
print('Numar observatii asteptate:', 84 * 3);

// ================================================
// 7. AFISAM PUNCTELE SI LACURILE
// ================================================

Map.addLayer(
  ee.FeatureCollection([
    ee.Feature(techirghiol),
    ee.Feature(amara),
    ee.Feature(nuntasi)
  ]).style({
    color: 'yellow',
    fillColor: '00000000',
    width: 2
  }),
  {},
  'Contururi lacuri'
);

Map.addLayer(
  puncte,
  {color: 'red'},
  'Puncte ERA5-Land'
);

Map.setCenter(28, 44.4, 8);

// ================================================
// 8. EXPORTAM REZULTATELE
// ================================================

Export.table.toDrive({
  collection: rezultate,
  description: 'CP1_ERA5_Lacuri_2015_2021',
  fileNamePrefix: 'CP1_ERA5_Lacuri_2015_2021',
  fileFormat: 'CSV',
  selectors: [
    'lac',
    'data',
    'an',
    'luna',
    'temperatura_medie_c',
    'precipitatii_totale_mm'
  ]
});
