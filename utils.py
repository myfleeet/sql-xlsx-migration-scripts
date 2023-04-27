import json

from data import (
  fuel_codes, transmission_codes, brands_codes, almacen_codes, status_venta_codes, disponibilidad_codes, store_codes
  )

"""
HELPER FUNCTIONS
"""

def rm_chars(str): 
  return ''.join(
    [char for char in str if char not in [" ", ".", "-", "_", "(", ")"]]
  )

def date_format(date): 
  return date.strftime("%Y%m%d") if date else None

def is_b2b(elm):
  return user_type(elm) == 'b2b'

def json_to_str(elm):
  return json.dumps(elm)

"""
SERIALIZER FUNCTIONS
"""

# MAKE - MODEL - VERSION

def family_code(elm):
  return rm_chars(elm['model'].upper())[:3]

def family_desc(elm):
  return elm['model'].upper()

def brand_astara_dist(elm):
  make_key = elm['make'].lower().replace(" ", "")
  return brands_codes[make_key] if make_key in brands_codes else None

def commercial_model(elm):
  return rm_chars(elm['model'].upper())[:18]

def version_code(elm):
  return rm_chars(elm['version'].upper())[:19] if elm['version'] else None

def make_model(elm):
  return f"{elm.get('make')} {elm.get('model')}".rstrip()

def material_code(elm):
  return elm['make'].upper().replace(" ", "") + elm['model'].upper().replace(" ", "")



# HUBS

def hub_code(elm):
  return almacen_codes.get(elm['hub_name'])

def hub_status_venta(elm):
  return status_venta_codes["Reservado"] if elm['status'] == 'booked' else None

def hub_disponibilidad(elm):
  if elm['status'] == 'booked':
    return disponibilidad_codes["Reservado"]
  if elm['status'] == 'in_catalog':
    return disponibilidad_codes["en catalogo"]
  if elm['status'] == 'pending_validation':
    return disponibilidad_codes["por validar"]



# CLIENTS

def user_type(elm):
  return store_codes.get(elm['store'])

def user_address(elm):
  return elm['billing_address'].get('address') if (elm['billing_address']) else None

def user_address_details(elm):
  return elm['billing_address'].get('address_details') if (elm['billing_address']) else None

def user_city(elm):
  return elm['billing_address'].get('municipality') if (elm['billing_address']) else None

def user_material_code(elm):
  return elm['billing_address'].get('zip_code') if (elm['billing_address']) else None

def user_newsletter(elm):
  return str(elm['subscribed_to_newsletter'])



# VEHICLES

def color_code(elm):
  return elm['color'].upper().replace(" ", "")[:3] if elm['color'] else None

def color_desc(elm):
  return elm['color'].lower() if elm['color'] else None

def shift_code(elm):
  return transmission_codes[elm['shift'].lower()] if (elm['shift'] and elm['shift'].lower() in transmission_codes) else None

def shift_desc(elm):
  return elm['shift'].lower() if elm['shift'] else None

def fuel_code(elm):
  fuel_value = fuel_desc(elm)
  return list(fuel_codes.keys())[list(fuel_codes.values()).index(fuel_value)] if fuel_value in fuel_codes.values() else None

def fuel_desc(elm):
  return elm['fuel_type'].lower() 

def vh_tags(elm):
  return (',').join(elm['tags'])

def vh_is_highlighted(elm):
  return str(elm['highlight_vehicle']) if elm['highlight_vehicle'] else None

def vh_calculated_autonomy(elm):
  return float(elm['fuel_tank']) * float(elm['consumption']) if (elm['fuel_tank'] and elm['consumption']) else None

def vh_accesories(elm):
  omit_specs = ['fuel_type', 'fuel_efficiency', 'fuel_capacity', 'electric_range', 'charging_time', 'engine_power', 'cargo_volume', 'height', 'width', 'length', 'co2_emissions', 'shift', 'traction', 'number_of_doors', 'seating_capacity', 'size', 'energy_label', 'environmental_label']
  return (',').join([
      str(key) + ':' + (str(value) if value else 'True') 
      for key, value 
      in elm['accessories'].items() 
      if key not in omit_specs
    ]) if elm['accessories'] else None


# PROFESSIONAL

def user_b2b_name(elm):
  if is_b2b(elm):
    return None
  
def user_b2b_first_name(elm):
  if is_b2b(elm):
    return elm.get('contact_person')
  
def user_b2b_last_name(elm):
  if is_b2b(elm):
    return None
  
def user_b2b_cif(elm):
  if is_b2b(elm):
    return elm.get('cif')