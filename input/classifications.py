output_file = 'Astara Move - Classifications'

query = """
SELECT 
    vc.make, 
    vc.model, 
    TRIM(vc."version") as "version",
    v.color, 
    vc.specs ->> 'fuel_type' AS fuel_type,
    vc.specs ->> 'environmental_label' AS environmental_label,
    vc.specs ->> 'shift' AS shift
FROM vehicles v, vehicle_classifications vc 
WHERE vc.id = v.vehicle_classification_id
GROUP BY 
    vc.make, 
    vc.model, 
    "version",
    v.color,
    vc.specs ->> 'fuel_type',
    vc.specs ->> 'environmental_label',
    vc.specs ->> 'shift'
ORDER BY 
    vc.make;
"""

mock_query_response = dict(
 make='Subaru', model='', version='', color='', fuel_type='', environmental_label='', shift=''
)

fuel_code = dict(
  D='diesel',
  G='gasoline',
  HEV='hev',
  E='electric',
  BD='biodiesel',
  PHE='pheveco',
  GLP='glp',
)

transmission_code = dict(
  automatic='A',
  manual='M'
)

brands_code = dict(
  subaru='01', 
  ssangyong="02",
  mitsubishi="03",
  maxus="04"
) 

def serialized_data(elm = mock_query_response):
  make_key = elm['make'].lower().replace(" ", "")
  fuel_value = elm['fuel_type'].lower()
  rm_chars = lambda str: ''.join([char for char in str if char not in [" ", ".", "-", "_", "(", ")"]])

  return {
    # ok - FLET
    'company code': 'FLET',

    # ok - AM
    'division':'AM',

    # ok - MAKE
    'vehicle brand':elm['make'].upper(),

    # ok - MODEL
    'family code for vehicle':elm['model'].upper(),

    # ok- MODEL
    'designation of family of vehicle':elm['model'].upper(), 

    # ok - MAKEMODEL
    'material number':elm['make'].upper().replace(" ", "") + elm['model'].upper().replace(" ", ""),

    # ok - MAKE + MODEL + VERSION
    'material description (short text)': elm['make'] + ' ' + elm['model'] + ' ' + elm['version'] if (elm['make'] and elm['model'] and elm['version']) else elm['make'] + ' ' + elm['model'],

    # ok - MY23
    'model year by vehicle model':'MY23',

    # ok - 2023
    'model year description':2023,

    # ok - VER -> 20 PRIMEROS CARACTERES VERSION SIN ESPACIO EN MAYUSCULAS
    'finishing / version by model and model year':rm_chars(elm['version'].upper())[:19] if elm['version'] else None,
    
    # ok - VERSION
    'version description of model vehicle':elm['version'] if elm['version'] else None,
    
    # ok - COL -> (COLOR upper, :3)
    'paint code for the vehicle model':elm['color'].upper().replace(" ", "")[:3] if elm['color'] else None,
    
    # ok - color
    'description of paint code':elm['color'].lower() if elm['color'] else None,

    'upholstery code associated with vehicle model':None,

    'description of upholstery':None, 
    
    # ok - fuel_code KEY
    'fuel code':list(fuel_code.keys())[list(fuel_code.values()).index(fuel_value)] if fuel_value in fuel_code.values() else None,
    
    # ok - fuel_code VALUE
    'fuel description':fuel_value, 
    
    # XX - transmission_code KEY
    'transmission code':transmission_code[elm['shift'].lower()] if (elm['shift'] and elm['shift'].lower() in transmission_code) else None, 
    
    # ok - transmission_code VALUE
    'transmission description':elm['shift'].lower() if elm['shift'] else None, 
    
    'customer warranty type':None,

    'supplier warranty type':None,

    # ok - 1
    'active record indicator (1 = active, 0 = not active)':1,
    
    # ok - active_record_indicator_code VALUE
    'brand from astara distribution':brands_code[make_key] if make_key in brands_code else None, 
  }