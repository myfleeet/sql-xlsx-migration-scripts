import utils

output_file = 'Subscription Loading Layout'

query = """
select 
	s.id as sub_id,
	s.client_id,
	s.status,
	vc.make,
	vc.model,
	vc."version",
	si.color,
	v.vin,
	-- DELIVERY 
	va.delivery_address, -- if !== HUBS type is door-to-door
	va.delivery_at,
	va.delivery_note,	
	-- PICK UP 
	s.cancel_requested_at,
	va.pick_up_address, -- if !== HUBS type is door-to-door
	va.pick_up_at,
	v.insurance_by,
	v.insurance_cost, 
	pm.method_type,
	c.failed_scoring,
	-- SUB
	pd.base_amount,
	s.subscription_pack_period,
  s.subscription_pack_price,
	c2.code,
	c2.amount_off,
	c2.percent_off,
	s.attached_documents
from subscriptions s 
left join vehicle_assignments va on va.subscription_id = s.id 
left join subscription_items si on si.subscription_id  = s.id
left join vehicle_classifications vc on si.vehicle_classification_id = vc.id
left join vehicles v on va.vehicle_id = v.id
left join payment_details pd on pd.subscription_id = s.id
left join payment_methods pm on pd.payment_method_id = pm.id
left join clients c on s.client_id = c.id
left join coupons c2 on pd.coupon_id = c2.id
;
"""

mock_query_response = dict(
  sub_id='',
  client_id='',
  status='',
  make='',
  model='',
  version='',
  color='',
  vin='',
  delivery_address='',
  delivery_at='',
  delivery_note='',
  cancel_requested_at='',
  pick_up_address='',
  pick_up_at='',
  insurance_by='',
  insurance_cost='',
  method_type='',
  failed_scoring='',
  base_amount='',
  subscription_pack_period='',
  subscription_pack_price='',
  code='',
  amount_off='',
  percent_off='',
  attached_documents='',
)

def serialized_data(elm = mock_query_response):
  return {
    'SubscriptionMoveId': elm.get('sub_id'),
    'SubscriptionSFDCId': None,
    'CustomerMoveId': elm.get('client_id'),
    'CustomerSFDCId': None,
    'CompanyCode': None,
    'Status': elm.get('status'),
    'Substatus': None,
    'SubscriptionOrigin': None,
    'Brand': elm.get('make'),
    'family': elm.get('make'),
    'model': elm.get('model'),
    'version': elm.get('version'),
    'modelyear': '🔴',
    'color': elm.get('color'),
    'upholstery': None,
    'VIN': elm.get('vin'),
    'deliveryType': utils.type_of_delivery(elm.get('delivery_address')),
    'deliveryDate': utils.time_format(elm.get('delivery_at')),
    'DeliveryHour': utils.hours_format(elm.get('delivery_at')),
    'DeliveryPickupaddress': utils.normalize_address(elm.get('delivery_address')),
    'DeliveryComments': elm.get('delivery_note'),
    'RequestReturnDate': elm.get('cancel_requested_at'),
    'PlannedReturnDate': elm.get('cancel_requested_at'),
    'returnDate': utils.time_format(elm.get('pick_up_at')),
    'returnHour': utils.hours_format(elm.get('pick_up_at')),
    'returnAddress': utils.normalize_address(elm.get('pick_up_address')),
    'ReturnType': utils.type_of_delivery(elm.get('pick_up_address')),
    'pickupDate': elm.get('pick_up_at'),
    'insurance': elm.get('insurance_by'),
    'paymentMethod': elm.get('method_type'),
    'EndingReason': None,
    'scoring': None,
    'ProbIncumplimientoScore': 'True' if elm.get('failed_scoring') else None,
    'Nota': None,
    'Decil': '🔴',
    'Percentil': '🔴',
    'deposit': '🔴',
    'period': elm.get('subscription_pack_period') or 1,
    'extraInsuranceCost': elm.get('insurance_cost'), # EXTRA ? 
    'subscriptionCost': elm.get('subscription_pack_price') if elm.get('subscription_pack_period') else elm.get('base_amount'),
    'PromoCode': elm.get('code'),
    'PromoDisccount': utils.promo_discount(elm),
    'Comments': '🔴',
    'History Json': '🔴',
    'Current Contracts': utils.json_to_str(elm.get('attached_documents')),
  }

