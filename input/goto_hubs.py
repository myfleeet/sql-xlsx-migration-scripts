import utils.utils as utils

output_file = 'Hub Layout'

query = """
select
	h.id,
	h.name,
	h.address,
	h.main_hub,
	h.type,
	h.vehicle_max_capacity,
	h.schedule
from hubs h
;
"""

mock_query_response = dict( 
  id='',
  name='Hub Madrid Norte',
  address='',
  main_hub='',
  type='',
  vehicle_max_capacity='',
  schedule='',
)

def serialized_data(elm = mock_query_response):
  return {
    'Hub ID': elm.get('id'),
    'Name': elm.get('name'),
    'Address': elm.get('address'),
    'Address Longitude ': utils.hub_coordinate(elm).get('long'),
    'Address latitude ': utils.hub_coordinate(elm).get('lat'),
    'Is Main': 'true' if elm.get('main_hub') else None,
    'Type': elm.get('type'),
    'Capcity Max': elm.get('vehicle_max_capacity'),
    'Open Times': elm.get('schedule'),
    'IsMain': 'true' if elm.get('main_hub') else None,
  }

