import utils

output_file = 'Subscriber Loading Layout'

query = """
select 
	c.id,
	c."name",
	c.surnames,
	c.email,
	c.phone,
	-- personal phone
	-- birthday
	c.billing_address,
	-- gdpr brand
	-- gdpr dealer
	-- company name
	c.cif 
from subscriptions s 
join clients c on s.client_id = c.id 
where
	-- 🔴 STATUS ???
	s.status = 'active'
; 
"""

mock_query_response = dict( 
  id='', name='', surnames='', email='', phone='', billing_address='', cif='',
)

def serialized_data(elm = mock_query_response):
  return {
    # Deben ser subscripciones activas ?

    'CustomerMoveId': elm.get('id'),
    
    # Dé dónde sacamos esto?
    'SalesforceId': '🔴',
    
    'FirstName': elm.get('name'),
    'LastName': elm.get('surnames'),
    'PersonEmail': elm.get('email'),
    
    # Duplicamos ? 
    'Phone': '🔴', 

    'Mobilephone': elm.get('phone'),
    'BirthDate': None,
    'PersonMailingCountryCode': 'ES',
    'PersonMailingStreet': f"{utils.user_address(elm)} {utils.user_address_details(elm)}",
    'PersonMailingCity': utils.user_city(elm),
    'PersonMailingPostCode': utils.user_material_code(elm),

    # Qué es esto?
    'GDPR Brand': '🔴', 
    'GDPR Dealer': '🔴', 

    # Sirve el nombre?
    'CompanyName': '🔴', 
    
    
    'documentType': 'CIF',
    'documentNumber': elm.get('cif'),
    'territory': 'ES',
  }