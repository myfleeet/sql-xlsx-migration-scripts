import utils

output_file = 'Astara Move - Stock in Service'

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
	c.name as client_name,
	v.created_at, 
	v.license_plate,
	lower(trim(v.color)) as color,
	trim(vc.specs ->> 'shift') AS shift,
	trim(vc.specs ->> 'fuel_type') AS fuel_type
from 
	vehicles v, 
	suppliers s, 
	hubs h, 
	vehicle_classifications vc, 
	vehicle_assignments va, 
	subscriptions s2,
	clients c 
where 
	s.id = v.supplier_id 
	and v.hub_id = h.id  
	and vc.id = v.vehicle_classification_id
	and va.vehicle_id = v.id
	and va.subscription_id = s2.id
	and s2.client_id = c.id
	and v.status IN ('in_service', 'logistic_ready_to_return_to_supplier', 'pending_client_check', 'with_issue', 'with_issue_waiting_repair')
;
"""

mock_query_response = dict(
  vin='', make='', model='', version='', cif='', hub_name='', location='', status='', client_name='', created_at='', license_plate='', color='', shift='', fuel_type=''
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

    # Problema con el JOIN 
    'nif_de_cliente': '🔴',

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

    # Problema con el JOIN
    "fecha_de_entrega_prevista": '🔴',

    "almacen_actual": utils.hub_code(elm),

    # De dónde sale este dato?
    "codigo_de_solicitante": '🔴',

    "codigo_de_destinatario": utils.hub_code(elm),
    "fecha_de_entrega_concesionario": None,
    "fecha_de_entrega_cliente_final": None,
    "fecha_confirmada_de_venta": None,
    "fecha_ultima_entrada_vo": None,
    "llaves": None,
    "motor": None,
    "pin_radio": None,

    # Confirmar valor
    "precio compra": '🔴',

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