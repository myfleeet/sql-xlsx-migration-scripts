import utils.utils as utils

output_file = 'Charact_PA_Model'

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
    'Gran Modelo': utils.commercial_model(elm),
    'Denominacion valor de  caracteristica': elm.get('model'),
  }