import utils.utils as utils

output_file = 'User Loading Layout'

query = """
select
	c.id,
	c.email,
	c.store,
	c."name",
	c.surnames,
	c.cif, 
	c.phone,
	c.billing_address,
	c.contact_person,
	c2.password_digest,
	c.can_leave_country,
	c.can_pay_with_sepa,
	c.can_do_same_day_subscriptions 
from clients c
left join credentials c2 on c.credentials_id = c2.id
; 
"""

mock_query_response = dict(
  id='',
  email='',
  store='',
  name='',
  surnames='',
  cif='',
  phone='',
  billing_address='',
  contact_person='',
  password_digest='',
  can_leave_country='',
  can_pay_with_sepa='',
  can_do_same_day_subscriptions='',
)

def serialized_data(elm = mock_query_response):
  return {
    'CustomerMoveId': elm.get('id'),
    'Email': elm.get('email'),
    'user type (b2b/b2c)': elm.get('store'),
    'User status (active/not active/etc..)': 'active',
    'email verified': 'True',
    'first name': elm.get('name'),
    'last name': elm.get('surnames'),
    'phone number': elm.get('phone'),
    'address': f"{utils.user_address(elm)} {utils.user_address_details(elm)}",
    'city ': utils.user_city(elm),
    'postcode': utils.user_material_code(elm),
    'country': 'ES',
    'state': utils.user_city(elm),
    'confirm recevie email': 'True',
    'company name': None,
    'contact person first name': elm.get('contact_person'),
    'contact person last name': None,
    'CIF': elm.get('cif'),
    'Phone': None,
    'Mobilephone': elm.get('phone'),
    'BirthDate': None,
    'PersonMailingCountryCode': 'ES',
    'PersonMailingStreet': f"{utils.user_address(elm)} {utils.user_address_details(elm)}",
    'PersonMailingCity': utils.user_city(elm),
    'PersonMailingPostCode': utils.user_material_code(elm),
    'GDPR Brand': None,
    'GDPR Dealer': None,
    'documentType': 'CIF',
    'territory': 'ES',
    'Hashed Password': elm.get('password_digest'),
    "allowLeaveTerritory": 'True' if elm.get('can_leave_country') == True else '',
    "allowSEPA": 'True' if elm.get('can_pay_with_sepa') == True else '',
    "ignoreMarginOnDays": 'True' if elm.get('can_do_same_day_subscriptions') == True else '',
  }

