import utils

output_file = 'Astara Move - Stock in Service'

query = """
select 
  c.cif as client_cif,
	v.vin, 
	vc.make, 
	vc.model, 
	vc.version,
	s.id as sub_id, 
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
left join suppliers s on v.supplier_id = s.id -- 990
left join hubs h on v.hub_id = h.id --990
left join vehicle_classifications vc on v.vehicle_classification_id = vc.id  -- 990
left join vehicle_assignments va on va.vehicle_id = v.id -- 881
left join subscriptions s2 on va.subscription_id = s2.id -- 881
left join clients c on s2.client_id = c.id -- 881
where  
	v.status IN ('in_service', 'logistic_ready_to_return_to_supplier', 'pending_client_check', 'with_issue', 'with_issue_waiting_repair') and
	va.delivery_at is not null and
	va.unassigned_at is null and
	va.pick_up_at is null
order by
  vc.model
;
"""

mock_query_response = dict(
  vin='',
  make='',
  model='',
  version='',
  sub_id='',
  cif='',
  hub_name='',
  location='',
  status='',
  client_cif='',
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
    "status_de_venta": 'ES01',
    'disponibilidad': 'ES', 
    'nif_de_cliente': elm.get('client_cif'),
    "emplazamiento": "CIRCULANDO",
    "utilizacion": "S1",
    "sub_utilizacion_o_departame": None,
    "fecha_de_primera_matricula": utils.date_format(elm['created_at']),
    "matricula": elm.get('license_plate'),
    "identificacion_de_vehiculo_usado": None,
    "estado_aduanero": '05',
    "estado_logistico": '01',
    "origen_mercancia": "IMPORT",
    "tipo_de_facturacion": None,
    "fecha_inventario": None,
    "fecha_retirada_de_vehiculo": None, 
    "tipo_de_riesgo": None,
    "fecha_produccion": utils.date_format(elm['created_at']),
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