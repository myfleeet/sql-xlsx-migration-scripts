import utils

output_file = 'User Loading Layout'

query = """
select 
	c.email,
	c.store,
	c."name",
	c.surnames,
	c.cif,
	c.phone,
	c.billing_address,
  c.subscribed_to_newsletter,
  c.contact_person
from clients c 
join credentials c2 on c.credentials_id = c2.id 
; 
"""

mock_query_response = dict( 
  email='',
  store='',
  name='',
  surnames='',
  cif='',
  phone='',
  billing_address='',
  subscribed_to_newsletter='',
  contact_person='',
)

def serialized_data(elm = mock_query_response):
  return {
    'Email': elm['email'],
    'user type (b2b/b2c)': utils.user_type(elm),
    'User status (active/not active/etc..)': 'true',
    'email verified': 'true',
    'first name': elm.get('name'),
    'last name': elm.get('surnames'),
    'id number': elm.get('cif'),
    'phone number': elm.get('phone'),
    'address': f"{utils.user_address(elm)} {utils.user_address_details(elm)}",
    'city ': utils.user_city(elm),
    'postcode': utils.user_material_code(elm),
    'country': 'Spain',
    'state': utils.user_city(elm),
    'confirm recevie email': utils.user_newsletter(elm),
    'company name': utils.user_b2b_name(elm),
    'contact person first name': utils.user_b2b_first_name(elm),
    'contact person last name': utils.user_b2b_last_name(elm),
    'CIF': utils.user_b2b_cif(elm),
  }

