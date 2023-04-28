import utils

output_file = 'Astara Move - Used Vehicle Stock'

query = """
select 
	v.status,
	v.vin,
	vc.make,
	vc.model,
	vc.version,
	s.cif,
	h."name" as hub_name,
	v.created_at,
	v.license_plate,
	lower(trim(v.color)) as color,
	trim(vc.specs ->> 'shift') AS shift,
	trim(vc.specs ->> 'fuel_type') AS fuel_type
from vehicles v 
left join vehicle_classifications vc on v.vehicle_classification_id = vc.id
left join suppliers s on v.supplier_id = s.id
left join hubs h on v.hub_id = h.id -- 69
where
	v.status in ('on_sale')
;
"""

mock_query_response = dict(
  status='',
  vin='',
  make='',
  model='',
  version='',
  cif='',
  hub_name='',
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
    'Material': utils.commercial_model(elm),
    'MATERIAL': utils.make_model(elm),
    'NIF_Proveedor': elm.get('cif'),
    'Centro': 'FESP',
    'Almacen': utils.hub_code(elm),
    'status_de_compra': 'ZZZ3',
    'status_de_venta': '🔴 ES01',
    'Disponibilidad': '🔴 DI',
    'NIF_de_cliente': '🔴 Empty',
    'Emplazamiento': 'Hub',
    'utilizacion': 'Z7',
    'Sub_Utilizacion_o_Departame': None,
    'Fecha_de_primera_matricula': utils.date_format(elm['created_at']),
    'matricula': elm.get('license_plate'),
    'Identificacion_de_vehiculo_usado': None,
    'estado_aduanero': '05',
    'estado_logistico': '01',
    'Origen_mercancia': 'IMPORT',
    'Tipo_de_facturacion': None,
    'fecha_inventario': None,
    'fecha_retirada_de_vehiculo': None,
    'tipo_de_riesgo': None,
    'Fecha_produccion': '🔴',
    'fecha_de_entrega_prevista': '🔴',
    'Almacen_actual': utils.hub_code(elm),
    'Codigo_de_Solicitante': '🔴',
    'Codigo_de_Destinatario': '🔴',
    'Fecha_de_entrega_concesionario': None,
    'Fecha_de_entrega_Cliente_final': None,
    'Fecha_confirmada_de_venta': None,
    'Fecha_Ultima_entrada_VO': None,
    'Llaves': None,
    'motor': None,
    'Pin_radio': None,
    'Precio compra': None,
    'Marca': '🔴',
    'Familia': utils.family_code(elm),
    'Material': utils.material_code(elm),
    'Model Year': "MY2023",
    'Acabado': utils.version_code(elm),
    'Pintura': utils.color_code(elm),
    'Tapiceria': None,
    'Combustible ': utils.fuel_code(elm),
    'Transmision': utils.shift_code(elm),
  }