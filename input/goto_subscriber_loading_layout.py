import utils.utils as utils

output_file = 'Subscriber Loading Layout'

query = """
select 
  distinct c.id,
  c."name",
  c.surnames,
  c.email,
  c.phone,
  c.billing_address,
  c.cif 
from subscriptions s
left join clients c on c.id = s.client_id 
; 
"""

mock_query_response = dict( 
  id='',
  name='',
  surnames='',
  email='',
  phone='',
  billing_address='',
  cif='',
)

def serialized_data(elm = mock_query_response):
  return {
    'CustomerMoveId': elm.get('id'),
    'SalesforceId': None,
    'FirstName': elm.get('name'),
    'LastName': elm.get('surnames'),
    'PersonEmail': elm.get('email'),
    'Phone': None, 
    'Mobilephone': elm.get('phone'),
    'BirthDate': None,
    'PersonMailingCountryCode': 'ES',
    'PersonMailingStreet': f"{utils.user_address(elm)} {utils.user_address_details(elm)}",
    'PersonMailingCity': utils.user_city(elm),
    'PersonMailingPostCode': utils.user_material_code(elm),
    'GDPR Brand': None, 
    'GDPR Dealer': None, 
    'CompanyName': None, 
    'documentType': 'CIF',
    'documentNumber': elm.get('cif'),
    'territory': 'ES',
  }