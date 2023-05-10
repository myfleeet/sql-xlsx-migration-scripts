import utils.utils as utils

output_file = 'Charact_PA_Fuel'

query = """
select 
	distinct trim(vc.specs ->> 'fuel_type') AS fuel_type   
from
	vehicle_classifications vc
where
  vc.specs ->> 'fuel_type' is not null
order by
	fuel_type
;  
"""

mock_query_response = dict(
  fuel_type=''
)

def serialized_data(elm = mock_query_response):
  return {
    'Clave de idioma': 'ES',
    'Transmision': utils.fuel_code(elm),
    'Denominacion valor de  caracteristica': utils.fuel_desc(elm), 
  }

