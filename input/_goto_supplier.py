import utils

output_file = 'Suppliers Layout'

query = """
select 
	s.id,
	s.cif,
	s.contact_person, -- name if not
	s.created_at,
	s.email,
	s."name",
	s.phone,
	s.billing_address
from suppliers s 
;
"""

mock_query_response = dict( 
  id='', cif='', contact_person='', created_at='', email='', name='', phone='', billing_address='',
)

def serialized_data(elm = mock_query_response):
  return {
    'id': elm.get('id'),
    'cif': elm.get('cif'),

    # 🔴 Confirmar esta lógica
    'contact_person': elm['contact_person'] if elm['contact_person'] else elm['name'],

    'created_at': elm.get('created_at'),
    'email': elm.get('email'),
    'name': elm.get('name'),
    'phone': elm.get('phone'),
    'billing_address': utils.user_address(elm),
    'billingaddress_details': utils.user_address_details(elm),
    'billingmunicipality': utils.user_city(elm),
    'billingzip_code': utils.user_material_code(elm),
  }

