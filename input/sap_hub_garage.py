output_file = 'Astara Move - Service per Hub&Garages'

query = """
select 
  name, 
  type 
from hubs h ; 
"""

mock_query_response = dict(
  type='',
  name='',
)

def serialized_data(elm = mock_query_response):
  return {
    "type": elm.get('type'),
    "name of supplier": elm.get('name'),
    "service performed": 'inspection',
  }