import utils.utils as utils

output_file = 'Vehicle infromation'

query = """
select
	v.vin,
	v.id as vehicle_id,
	h."name" as hub_name,
	h.address as hub_address,
  	v.status,
	v.insurance_by,
	v.insurance_company,
	v.insurance_cost,
	v.current_tracker_id, 
	v.last_km,
	v.created_at,
	v.received_at,
	v.returned_at,
	v.returned_real_at,
	v.vehicle_type,
	v.license_plate,
	json_agg(
		json_build_object(
			'type', cr2.report ->> 'check_type',
			'created_at', cr2.created_at,
			'report', cr2.report
		) 
	) as reports
from vehicles v
left join (
	select 
		max(cr1.created_at) as created_at,
		cr1.vehicle_id,
		cr1.report
	from  (
		select 
			cr.vehicle_id,
			cr.created_at,
			cr.report
		from check_reports cr
		where 
			cr.report ->> 'check_type' in ('check-in', 'check-1', 'check-client', 'check-2')
	) cr1
	group by 
		cr1.vehicle_id, 
		cr1.report
) cr2 on v.id = cr2.vehicle_id
left join hubs h on h.id = v.hub_id
group by 
	v.vin,
	v.id,
	hub_name, 
	hub_address,
	v.status,
	v.current_tracker_id, 
	v.last_km, 
	v.insurance_by,
	v.insurance_company,
	v.insurance_cost,
	v.created_at,
	v.received_at,
	v.returned_at,
	v.returned_real_at,
	v.vehicle_type,
	v.license_plate
;
"""

"""
-- RETURN TOTAL OF CHECKS BY VH_ID
select 
	count(cr.vehicle_id) as counter,
	cr.vehicle_id
from check_reports cr
group by
	cr.vehicle_id 
order by 
	counter desc
; 


-- LATEST DESIRED CHECKS BY VH_ID
select 
	max(cr.created_at) as created_at,
	cr.report ->> 'check_type' as check_type,
	cr.vehicle_id 
from check_reports cr  
group by
	check_type,
	cr.vehicle_id
having
	cr.report ->> 'check_type' in ('check-in', 'check-1', 'check-client', 'check-2') and 
	cr.vehicle_id = 'cae5440c-8c3f-4979-92b0-743b8e61c61c'
order by
	created_at desc
;
"""

mock_query_response = dict(
  vin='',
  vehicle_id='',
  status='',
  hub_name='',
  hub_address='',
  insurance_by='',
  insurance_company='',
  insurance_cost='',
  current_tracker_id='',
  last_km='',
  reports=[],
  created_at='',
  received_at='',
  returned_at='',
  returned_real_at='',
  vehicle_type='',
  license_plate='',
)

def serialized_data(elm = mock_query_response):
  return {
    'VIN': elm.get('vin'),
    'Move Internal Vehicle ID': elm.get('vehicle_id'),
    'Hub name': elm.get('hub_name'),
    'Current status': elm.get('status'),
    "Vehicle type": elm.get('vehicle_type'),
    "License plate": elm.get('license_plate'),
    # Seguro
    'Aseguradora': elm.get('insurance_company'),
    'No poliza': None,
    'Asegurado por': elm.get('insurance_by'),
    'Precio poliza': elm.get('insurance_cost'),
    # IOT
    'astara connect id (oid)': elm.get('current_tracker_id'),
    'Current KM from connect': None, 
    'Current KM by operation team': elm.get('last_km'),
    'location latitude': utils.hub_coordinate(elm).get('lat'), # 🔴  doble check coordenadas in_catalog
    'location longitude': utils.hub_coordinate(elm).get('long'), # 🔴  doble check coordenadas in_catalog
    'location address': utils.hub_coordinate(elm).get('address'), # 🔴  doble check coordenadas in_catalog
    # Checks -> enlace y fecha de último (solo 1 ID por VH) # https://logistics.astaramove.com/vehicles/d1554884-fca4-4056-b161-f3f512021bd4/detail/
    'Check initial': utils.report_check(elm.get('reports')).get('check_in').get('created_at'),
    'check initial document': None,
    'Check client': utils.report_check(elm.get('reports')).get('check_client').get('created_at'),
    'check client document': None,
    # News
	'alta en logistica': elm.get('created_at'),
	'incorporacion a la flota': elm.get('received_at'),
	'devolucion prevista': elm.get('returned_at'),
	'devolucion definitiva': elm.get('returned_real_at'),
  }
 