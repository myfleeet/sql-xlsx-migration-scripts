import utils.utils as utils

output_file = 'Classfication Loading Layout'

query = """
select 
  string_agg(distinct ci.store, ', ') as store,
  ci.published,
  vc.vehicle_type,
  vc.make,
  vc.model,
  vc."version", 
  vc.id,
  lower(v.color),
  -- active in store
  vc.specs ->> 'fuel_type' as combustible, 
  vc.specs ->> 'fuel_efficiency' as consumption, -- ???
  vc.specs ->> 'fuel_capacity' as fuel_tank,
  -- autonomy
  vc.specs ->> 'electric_range' as electric_range,
  vc.specs ->> 'charging_time' as charging_time,
  vc.specs ->> 'engine_power' as max_power, -- ?? 
  vc.specs ->> 'cargo_volume' as cargo_volume,
  vc.specs ->> 'height' as height,
  vc.specs ->> 'width' as width,
  vc.specs ->> 'length' as width,
  -- van format
  vc.specs ->> 'co2_emissions' as co2_emissions,
  vc.specs ->> 'shift' as gear_type,
  vc.specs ->> 'traction' as traction,
  vc.specs ->> 'number_of_doors'as number_of_doors,
  vc.specs ->> 'seating_capacity' as number_of_seats,
  vc.specs ->> 'size' as size,
  upper(vc.specs ->> 'energy_label') as energy_classification,
  upper(vc.specs ->> 'environmental_label') as environmental_label,
  vc.specs as accessories
from vehicle_classifications vc  
left join vehicles v on v.vehicle_classification_id = vc.id 
join catalog_items ci on vc.id = ci.vehicle_classification_id
group by
  vc.vehicle_type, 
  vc.id,
  ci.published,
  vc.make,
  vc.model,
  vc."version",
  v.color
having
  v.color is not null
order by vc."version" 
;
"""

mock_query_response = dict( 
  vehicle_type='',
  make='',
  model='',
  version='',
  id='',
  color='',
  combustible='',
  consumption='',
  fuel_tank='',
  electric_range='',
  charging_time='',
  max_power='',
  cargo_volume='',
  height='',
  width='',
  length='',
  co2_emissions='',
  gear_type='',
  traction='',
  number_of_doors='',
  number_of_seats='',
  size='',
  energy_classification='',
  environmental_label='',
  accessories='',
  published='',
  store='', 
)

def serialized_data(elm = mock_query_response):
  return {
    'Vehicle Type': elm.get('vehicle_type'),
    'Brand (Manufacturer)': elm.get('make'),
    'Family': elm.get('make'),
    'Model': elm.get('model'),
    'Version': elm.get('version'),
    'Year': None, 
    'Company code': None, 
    'Exterior color': elm.get('color'),
    'Active in stores': elm.get('store'),
    'Combustible': elm.get('combustible'),
    'Consumption': elm.get('consumption'),
    'Fuel tank': elm.get('fuel_tank'),
    'Autonomy': utils.vh_calculated_autonomy(elm),
    'Electric range': elm.get('electric_range'),
    'Charging time': elm.get('charging_time'),
    'Maximum power': elm.get('max_power'),
    'Cargo volume': elm.get('cargo_volume'),
    'Height': elm.get('height'),
    'Length': elm.get('length'),
    'Width': elm.get('width'),
    'Van format': None, 
    'CO2 Emissions': elm.get('co2_emissions'),
    'Gear type': elm.get('gear_type'),
    'Traction': elm.get('traction'),
    'Number of doors': elm.get('number_of_doors'),
    'Number of seats': elm.get('number_of_seats'),
    'Size': elm.get('size'),
    'Energy classification': elm.get('energy_classification'),
    'Enviromental label': elm.get('environmental_label'),
    'Accessories': utils.vh_accesories(elm),
    'astaramove classfication id': elm.get('id'),
    'is Active': 'True' if elm.get('published') else None, 
  }

