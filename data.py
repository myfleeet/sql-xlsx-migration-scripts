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
  "Hub Barcelona":"AM03",
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