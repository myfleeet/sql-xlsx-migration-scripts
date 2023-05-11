import utils.utils as utils

output_file = 'Charact_PA_Transmission'

query = """
select 
	distinct trim(vc.specs ->> 'shift') AS shift   
from
	vehicle_classifications vc
where
  vc.specs ->> 'shift' is not null
order by
	shift
;  
"""

mock_query_response = dict(
  shift=''
)

def serialized_data(elm = mock_query_response):
  return {
    'Clave de idioma': 'ES',
    'Transmision': utils.shift_code(elm), 
    'Denominacion valor de  caracteristica': utils.shift_desc(elm), 
  }