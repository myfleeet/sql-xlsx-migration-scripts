output_file = 'Subscriber documents Loading Layout'

query = """
select 
  c.id as customer_id, 
  d.doc_name as doc_type, 
  (d.doc_value->>'url')::text AS doc_id, 
  (d.doc_value->>'status')::text AS doc_status
from
  clients c 
  cross join lateral jsonb_each(c.documents) AS d(doc_name, doc_value)
where 
  d.doc_value ? 'url' and 
  d.doc_value ? 'status'
order by
  c.id, 
  d.doc_name
;
"""

mock_query_response = dict(
  id='',
  documents=dict( 
    id_back=dict( url= "", status= "", created_at= "" )
  )
)

def serialized_data(elm = mock_query_response):
  return {
    'CustomerMoveId': elm.get('customer_id'),
    'CustomerSalesforceId': None,
    'DocId': elm.get('doc_id'),
    'DocType': elm.get('doc_type'),
    'DocStatus': elm.get('doc_status'),
  }