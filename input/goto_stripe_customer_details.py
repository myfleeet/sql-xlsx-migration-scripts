import utils.utils as utils

output_file = 'Stripe Customer Details'

query = """
select 
  distinct pm.customer_id,
  c.id,
  c."name",
  c.billing_address,
  c.email,
  c.cif,
  c.phone
from clients c
left join payment_methods pm on c.id = pm.client_id
order by pm.customer_id
;
"""

mock_query_response = dict(
  customer_id='',
  id='',
  name='',
  billing_address='',
  email='',
  cif='',
  phone=''
)

def serialized_data(elm = mock_query_response):
  return {
    'Astara move uniq ID': elm.get('id'),
    'ASTARA MOVE STRIPE ID': elm.get('customer_id'),
    'Name': elm.get('name'),
    'Address': f"{utils.user_address(elm)} {utils.user_address_details(elm)}",
    'Email': elm.get('email'),
    'ID No or passport': elm.get('cif'),
    'Phone': elm.get('phone'),
    'Zip': utils.user_material_code(elm),
  }