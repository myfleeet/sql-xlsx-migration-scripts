import utils.utils as utils

output_file = 'Charact_PA_Paint'

query = """
select 
	distinct lower(trim(v.color)) as color
from
	vehicles v
where
  color is not null
order by
	color
;  
"""

mock_query_response = dict(
  color=''
)

def serialized_data(elm = mock_query_response):
  return {
    'Clave de idioma': 'ES',
    'Pintura/External color': utils.color_code(elm),
    'Denominacion valor de  caracteristica': utils.color_desc(elm),
  }