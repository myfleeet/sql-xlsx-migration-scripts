import utils

output_file = 'Catalog Loading Layout'

query = """
select 
	vc.make,
	vc.model,
	vc.version,
	vc.id,
	ci.days_to_subscription, -- preguntar a Juanjo
	ci.days_max_to_subscription,
	ci.store,
	ci.image,
	ci.tags,
	ci.highlight_vehicle 
from 
	vehicle_classifications vc 
join catalog_items ci on ci.vehicle_classification_id = vc.id
;
"""

mock_query_response = dict( 
  make='', model='', version='', id='', days_to_subscription='', days_max_to_subscription='', store='', image='', tags='', highlight_vehicle='',
)

def serialized_data(elm = mock_query_response):
  return {
    # Cuál es este valor ? 
    'Classfication - company code':'🔴', 

    'Classfication Brand (Manufacturer)': elm.get('make'),
    'Classfication Family': utils.family_code(elm),
    'Classfication Model': elm.get('model'),
    
    # De dónde sale este valor ?
    'Classfication Year':'🔴', 
    
    'Classfication Version': elm.get('version'),
    'astaramove classficationid': elm.get('id'),
    
    # De dónde sale este valor ?
    'minimum days for start':'🔴', 
    
    'maximum days for start': elm.get('days_max_to_subscription'),
    'Store type': utils.user_type(elm),
    
    # De dónde sale este valor ?
    'CMS content':'🔴',
    
    'main image': elm.get('image'),
    'type of use': utils.vh_tags(elm),
    'is highlted ': utils.vh_is_highlighted(elm),
  }

