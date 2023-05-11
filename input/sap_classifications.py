import utils.utils as utils

output_file = 'Astara Move - Classifications'

query = """
select 
  vc.make, 
  vc.model, 
  TRIM(vc."version") as "version",
  lower(trim(v.color)) as color, 
  vc.specs ->> 'fuel_type' AS fuel_type,
  vc.specs ->> 'environmental_label' AS environmental_label,
  vc.specs ->> 'shift' AS shift
from vehicles v, vehicle_classifications vc 
where vc.id = v.vehicle_classification_id
group by
  vc.make, 
  vc.model, 
  "version",
  v.color,
  vc.specs ->> 'fuel_type',
  vc.specs ->> 'environmental_label',
  vc.specs ->> 'shift'
order by
  vc.make;
"""

mock_query_response = dict(
 make='Subaru', model='',
  version='',
  color='',
  fuel_type='',
  environmental_label='',
  shift=''
)

def serialized_data(elm = mock_query_response):  
  return {
    'company code': 'FLET',
    'division':'AM',
    'vehicle brand':elm.get('make').upper(),
    'family code for vehicle': utils.family_code(elm),
    'designation of family of vehicle': utils.family_desc(elm), 
    'material number': utils.commercial_model(elm),
    'material description (short text)': f"{elm.get('make')} {elm.get('model')} {elm.get('version')}".rstrip(),
    'model year by vehicle model':'MY23',
    'model year description':2023,
    'finishing / version by model and model year': utils.version_code(elm),
    'version description of model vehicle': elm.get('version'),
    'paint code for the vehicle model': utils.color_code(elm),
    'description of paint code': utils.color_desc(elm),
    'upholstery code associated with vehicle model':None,
    'description of upholstery':None, 
    'fuel code': utils.fuel_code(elm),
    'fuel description': utils.fuel_desc(elm), 
    'transmission code': utils.shift_code(elm), 
    'transmission description': utils.shift_desc(elm), 
    'customer warranty type':None,
    'supplier warranty type':None,
    'active record indicator (1 = active, 0 = not active)':1,
    'brand from astara distribution': utils.brand_astara_dist(elm), 
  }