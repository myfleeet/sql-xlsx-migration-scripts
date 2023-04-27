import utils

output_file = 'Astara Move - Stock in Hub'

query = """
select 
	v.vin, 
	vc.make, 
	vc.model, 
	vc.version, 
	s.cif, 
	h."name" as hub_name, 
	v."location", 
	v.status, 
	v.created_at, 
	v.license_plate,
	lower(trim(v.color)) as color,
	trim(vc.specs ->> 'shift') AS shift,
	trim(vc.specs ->> 'fuel_type') AS fuel_type
from vehicles v
left join suppliers s on s.id = v.supplier_id
left join hubs h on v.hub_id = h.id
left join vehicle_classifications vc on vc.id = v.vehicle_classification_id
where    
	v.status IN ('booked', 'in_catalog', 'pending_validation')
;
"""

mock_query_response = dict(
  vin='',
  make='',
  model='',
  version='',
  cif='',
  hub_name='',
  location='',
  status='',
  created_at='',
  license_plate='',
  color='',
  shift='',
  fuel_type=''
)

def serialized_data(elm = mock_query_response):
  return {
    'Seq_Num_de_linea': None, 
    'VHCLE': None, 
    'Num_Veh_Sist_Anterior': None,
    'VON': None,
    'VIN': elm.get('vin'),
    'Material(modelocoche)': utils.commercial_model(elm),
    'MATERIAL': utils.make_model(elm),
    'NIF_Proveedor': elm.get('cif'),
    'centro': 'FESP',
    'almacen': utils.hub_code(elm),
    "status_de_compra": "ZZZ3",
    "status_de_venta": utils.hub_status_venta(elm),
    'disponibilidad': utils.hub_disponibilidad(elm), 
    'nif_de_cliente': None, 
    "emplazamiento": "Hub",
    "utilizacion": "S1",
    "sub_utilizacion_o_departame": None,
    "fecha_de_primera_matricula": utils.date_format(elm.get('created_at')),
    "matricula": elm.get('license_plate'),
    "identificacion_de_vehiculo_usado": None,
    "estado_aduanero": '05',
    "estado_logistico": '01',
    "origen_mercancia": "IMPORT",
    "tipo_de_facturacion": None,
    "fecha_inventario": None,
    "fecha_retirada_de_vehiculo": None, 
    "tipo_de_riesgo": None,
    "fecha_produccion": utils.date_format(elm.get('created_at')),
    "fecha_de_entrega_prevista": None, 
    "almacen_actual": utils.hub_code(elm),
    "codigo_de_solicitante": None,
    "codigo_de_destinatario": utils.hub_code(elm),
    "fecha_de_entrega_concesionario": None,
    "fecha_de_entrega_cliente_final": None,
    "fecha_confirmada_de_venta": None,
    "fecha_ultima_entrada_vo": None,
    "llaves": None,
    "motor": None,
    "pin_radio": None,
    "precio compra": None,
    "marca": elm.get('make'),
    "familia": utils.family_code(elm),
    "material": utils.material_code(elm),
    "model year": "MY2023",
    "acabado": utils.version_code(elm),
    "pintura": utils.color_code(elm),
    "tapiceria": None,
    "combustible": utils.fuel_code(elm),
    "transmision": utils.shift_code(elm),
  }