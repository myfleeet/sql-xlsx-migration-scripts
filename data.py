fuel_codes = dict(
  D='diesel',
  G='gasoline',
  HEV='hev',
  E='electric',
  BD='biodiesel',
  PHE='pheveco',
  PHEC='phevcero',
  GLP='glp',
)

transmission_codes = dict(
  automatic='A',
  manual='M'
)

brands_codes = dict(
  subaru='01', 
  ssangyong="02",
  mitsubishi="03",
  maxus="04"
)

almacen_codes = {
  "Hub Madrid Norte":"AM01",
  "Hub Madrid Sur":"AM02",
  "Campa Leganés":"AM02",
  "Hub Barcelona":"AM03",
}

hub_coordinates = {
  'Hub Madrid Norte': dict(
    address='Calle de los Aragoneses, 3, 28108 Alcobendas, Madrid, España',
    lat='40.52382424994542',
    long='-3.6599958886963257',
  ),
  'Hub Madrid Sur': dict(
    address='Avenida Carlos Sainz, 51, 28914 Leganés, Madrid, España.',
    lat='40.313687799470365',
    long='-3.772986990552989',
  ),
  'Campa Leganés': dict(
    address='Calle Ricardo Tormo, 102, Leganés, España.',
    lat='40.309065419102126',
    long='-3.776312190553207',
  ),
  'Hub Barceloneta Port Vell': dict(
    address='Plaza de Pau Vila, 1, 08039 Barcelona, España.',
    lat='41.38098447272121',
    long='2.185338496007691',
  ),
  'Campa Mollet': dict(
    address='Avinguda de Can Prat, no 15, 08100 Mollet del Vallès, Barcelona, España.',
    lat='41.539726362766935',
    long='2.223304986213112',
  ),
}

status_venta_codes = dict(
  Reservado="RR01",
)

disponibilidad_codes =  {
  "por validar" :"PV",
  "en catalogo":"LC",
  "Reservado":"RR"
}

estado_aduanero_codes = {
  '00': 'EXENTO',
  '01': 'PENDIENTE (Embarcado)',
  '02': 'PENDIENTE (Recibido DS)',
  '03': 'SOLICITADO',
  '04': 'EN EXPEDIENTE',
  '05': 'DESPACHADO',
  '06': 'SOLIC. DEPÓSITO',
  '10': 'DEPOSITO ADUANERO',
  '12': 'TRANSITO ADUANERO"'
}

store_codes = dict(
  cardive='b2c',
  fleeet='b2b',
)

normalize_astara_addresses = {
  'Av. de Bruselas, 32, 28108 Alcobendas, Madrid': [
    'brusleas 20',
    'brusel',
  ],
  'Calle de los Aragoneses, 3, 28108 Alcobendas, Madrid, España': [
    'arsgoneses 3 alcobendas',
    'aragoses 3',
    'aragonés 3 ',
    'aradoneses',
    'calle ragoneses 3 alcobendas',
    'aragone',
    'aragoné'
    'astara',
    'nave alcobendas',
    'nave-alcobendas',
    'nave, alcobendas',
    'calle a4agoneses 3, madrid.',
    'nave fleeet',
    'nave.'
  ],
  'Avenida Carlos Sainz, 51, 28914 Leganés, Madrid, España': [
    '51 53',
    'carlos sa',
    'nave leganés',
    'campa de leganes',
    'campa legan',
    'está en legan',
    'el coche está en leganes', 
    'leganés avenida carlos 52 53',
    'leganés, avenida  carlos  sainz 51',
    'legenés',
    'vehículo en leganes',
    'leganes.',
    'leganés, españa',
    # 
    'grupo más-avenida carlos  sainz,51-leganés',
    'grupo más, avenida carlos 51, leganés'
  ],
  'Calle Ricardo Tormo, 102, Leganés, España': [],
  'Plaza de Pau Vila, 1, 08039 Barcelona, España': [],
  'Avinguda de Can Prat, no 15, 08100 Mollet del Vallès, Barcelona, España': []
}

