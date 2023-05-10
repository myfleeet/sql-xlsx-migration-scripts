import utils.utils as utils

output_file = 'Active Subscription History'

query = """
select 
	s.started_at,
	s.id, -- public_id, idempotency_key
	s.pick_up_details as msg_link_1,
	s.delivery_details as msg_link_2,
	s.attached_documents as msg_file,
	s.status
from subscriptions s
-- where s.status not in ('ended', 'start_pending') -- se está conversando
order by s.started_at desc
;
"""

mock_query_response = dict(
  started_at='',
  id='',
  msg_link_1='',
  msg_link_2='',
  msg_file='',
  status='',
)

# https://logistics-staging.astaramove.com/subscriptions/cbd5564b-e457-4882-bf9b-d8b7bb30ef04/history
def serialized_data(elm = mock_query_response):
  return {
    'date': elm.get('started_at'),
    'subscriptionid': elm.get('id'), 
    'description': '🔴',
    'message': '🔴',
    'messge type': utils.message_type(),
    'message link ID1': utils.json_to_str(elm.get('msg_link_1')),
    'message link ID2': utils.json_to_str(elm.get('msg_link_2')),
    'message file link': utils.json_to_str(elm.get('msg_file')),
    'state': elm.get('status'),
  }
