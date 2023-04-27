import utils

output_file = 'Catalog Loading Layout'

query = """
select 
  vc.make,
  vc.model,
  vc.version,
  vc.id,
  ci.days_to_subscription,
  ci.days_max_to_subscription,
  ci.store,
  ci.image,
  ci.tags,
  ci.highlight_vehicle,
  ci.meta
from vehicle_classifications vc 
join catalog_items ci on ci.vehicle_classification_id = vc.id
;
"""

mock_query_response = dict( 
  make='',
  model='',
  version='',
  id='',
  days_to_subscription='',
  days_max_to_subscription='',
  store='',
  image='',
  tags='',
  highlight_vehicle='',
  meta=''
)

def serialized_data(elm = mock_query_response):
  return {
    'Classfication - company code': None, 
    'Classfication Brand (Manufacturer)': elm.get('make'),
    'Classfication Family': utils.family_code(elm),
    'Classfication Model': elm.get('model'),
    'Classfication Year': None, 
    'Classfication Version': elm.get('version'),
    'astaramove classficationid': elm.get('id'),
    'minimum days for start': elm.get('days_to_subscription'), 
    'maximum days for start': elm.get('days_max_to_subscription'),
    'Store type': utils.user_type(elm),
    'CMS content': utils.json_to_str(elm.get('meta')),
    'main image': elm.get('image'),
    'type of use': utils.vh_tags(elm),
    'is highlted ': utils.vh_is_highlighted(elm),
  }

