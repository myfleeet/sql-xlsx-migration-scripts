import utils.utils as utils

output_file = 'Charact_PA_Version'

query = """
select 
  distinct trim(vc."version") as "version"
from
	vehicle_classifications vc
order by
	"version"
;  
"""

mock_query_response = dict(
  version=''
)

def serialized_data(elm = mock_query_response):
  return {
    'Clave de idioma': 'ES',
    'Acabado': utils.version_code(elm),
    'Denominacion valor de  caracteristica': elm.get('version'),
  }