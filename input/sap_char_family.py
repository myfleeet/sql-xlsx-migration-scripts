import utils.utils as utils

output_file = 'Charact_PA_Family'

query = """
select 
  distinct trim(vc."model") as "model"
from
	vehicle_classifications vc
order by
	"model"
;
"""

mock_query_response = dict(
  model=''
)

def serialized_data(elm = mock_query_response):
  return {
    'Clave de idioma': 'ES',
    'Gran Modelo': utils.family_code(elm),
    'Denominacion valor de  caracteristica': utils.family_desc(elm) ,
  }