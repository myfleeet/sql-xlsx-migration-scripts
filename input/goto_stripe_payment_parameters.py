import utils.utils as utils

output_file = 'Stripe Payment Parameters'

query = """
select 
	pm.id,
	c.default_payment_method_id,
  c.id as client_id,
	pm.customer_id,
	pm.method_id,
	pm.method_type,
	pm.document_hint ->> 'exp_month' as exp_month,
	pm.document_hint ->> 'exp_year' as exp_year,
	pm.document_hint ->> 'brand' as brand,
	pm.document_hint ->> 'last4' as last4
from payment_methods pm
left join clients c on c.id = pm.client_id
;
"""

mock_query_response = dict(
  id='',
  customer_id='',
  method_id='',
  method_type='',
  exp_year='2023',
  exp_month='05',
  brand='',
  last4='',
  default_payment_method_id='',
  client_id='',
)


def serialized_data(elm = mock_query_response):
  return {
    'Astara move uniq ID PAYMENT METHOD': elm.get('id'),
    'Astara move uniq ID CUSTOMER': elm.get('client_id'),
    'ASTARA MOVE STRIPE ID': elm.get('customer_id'),
    'Stripe Payment Method ID': elm.get('method_id'),
    'Payment Type (Credit/SEPA)': elm.get('method_type'),
    'Expiration Date': utils.stripe_payment_expiration_format(elm),
    'Brand / BankCode': elm.get('brand'),
    'Last 4 digits': elm.get('last4'),
    "is default payment method": "true" if elm.get("default_payment_method_id") == elm.get("id") else None
  }