output_file = 'Stripe Payment Parameters'

query = """
select 
	pm.id,
	pm.customer_id,
	pm.method_id,
	pm.method_type,
	pm.document_hint ->> 'exp_year' as exp_year,
	pm.document_hint ->> 'brand' as brand,
	pm.document_hint ->> 'last4' as last4
from payment_methods pm
;
"""

mock_query_response = dict(
  id='',
  customer_id='',
  method_id='',
  method_type='',
  exp_year='',
  brand='',
  last4=''
)

def serialized_data(elm = mock_query_response):
  return {
    'Astara move uniq ID': elm.get('id'),
    'ASTARA MOVE STRIPE ID': elm.get('customer_id'),
    'Stripe Payment Method ID': elm.get('method_id'),
    'Payment Type (Credit/SEPA)': elm.get('method_type'),
    'Expiration Date': elm.get('exp_year'),
    'Brand / BankCode': elm.get('brand'),
    'Last 4 digits': elm.get('last4'),
  }