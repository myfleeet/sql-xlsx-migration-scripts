import json
from datetime import datetime

from utils.data import (
  fuel_codes, transmission_codes, brands_codes, 
  almacen_codes, status_venta_codes, disponibilidad_codes, 
  store_codes, normalize_astara_addresses, hub_coordinates,
  message_type_codes, vehicle_history_action_type_codes
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

def hours_format(date):
  return date.strftime("%H:%M") if date else None  

def time_format(date):
  return date.strftime("%Y/%m/%d") if date else None

"""
SERIALIZER FUNCTIONS
"""

# MAKE - MODEL - VERSION

def family_code(elm):
  model = [ rm_chars(x.upper()) for x in elm.get('model').strip().split(" ")]
  if len(model) == 1:
    if (model[0] in ['500E', 'OUTBACK', 'OUTLANDER', '5008', 'TRANSIT', 'TRANSPORTER', 'TWEET']):
      return model[0][:2] + model[0][-1:]
    return model[0][:3]
  if len(model) == 2:
    if (model[1] in ['CONNECT']):
      return model[0][:2] + model[1][:-1]
    return model[0][:2] + model[1][:1]
  if len(model) == 3:
    return model[0][:1] + model[1][:1] + model[2][:1]

def family_desc(elm):
  return elm['model'].upper().strip()

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
  return almacen_codes.get(elm['hub_name']) if elm.get('hub_name') else almacen_codes.get('Hub Madrid Norte')

def hub_name(elm):
  return elm.get('name')

def hub_status_venta(elm):
  return status_venta_codes["Reservado"] if elm['status'] == 'booked' else None

def hub_disponibilidad(elm):
  if elm['status'] == 'booked':
    return disponibilidad_codes["Reservado"]
  if elm['status'] == 'in_catalog':
    return disponibilidad_codes["en catalogo"]
  if elm['status'] == 'pending_validation':
    return disponibilidad_codes["por validar"]

def hub_coordinate(elm):
  return hub_coordinates.get(elm.get('name')) if hub_coordinates.get(elm.get('name')) else dict(long=None, lat=None)

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
  
# ADDRESS
def normalize_address(elm):
  if not elm:
    return None
  address = elm.lower().strip()
  for key in list(normalize_astara_addresses.keys()):
    for value in normalize_astara_addresses[key]:
      if value in address:
        return key
  return address

def type_of_delivery(elm = None):
  if not elm:
    return None
  address = normalize_address(elm)
  type = 'door_to_door'
  for key in list(normalize_astara_addresses.keys()):
    if address == key:
      type ='store'
  return type
    
def promo_discount(elm):
  if elm.get('amount_off'):
    return f"{elm.get('amount_off')} €" 
  if elm.get('percent_off'):
    return f"{elm.get('percent_off')} %"
  return None

def message_type(elm = None):
  # message_type_codes
  return '🔴'

def vh_action_type(elm = None):
  # vehicle_history_action_type_codes
  return None

#  Reports

def report_check(report):
  if not report: 
    return dict(
      check_in=dict(created_at=None, report_info={}), 
      check_client=dict(created_at=None, report_info={}),
    )

  check_in = {}
  check_client = {}
  
  for elm in report:
    check_type = elm.get('type')
    created_at = elm.get('created_at')
    report_info = elm.get('report')

    if check_type in ("check-in", "check-1"):
      if (
        not check_in.get('created_at') or
        (
          check_in.get('created_at') and
          datetime.fromisoformat(check_in.get('created_at')) < datetime.fromisoformat(created_at)
        )
      ):
        check_in.update({
          'created_at': created_at,
          'report_info': report_info,
        })

    if check_type in ("check-client", "check-2"):
      if (
        not check_client.get('created_at') or
        (
          check_client.get('created_at') and
          datetime.fromisoformat(check_client.get('created_at')) < datetime.fromisoformat(created_at)
        )
      ):
        check_client.update({
          'created_at': created_at,
          'report_info': report_info,
        })
      
  return dict(
    check_in=check_in if check_in else dict(created_at=None, report_info={}), 
    check_client=check_client if check_client else dict(created_at=None, report_info={}), 
    ) 