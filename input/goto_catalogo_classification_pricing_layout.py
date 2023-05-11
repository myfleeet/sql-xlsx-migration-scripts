output_file = 'Catalog classification Pricing Layout'

query = """
select
  vc.make,
  vc.model,
  vc."version",
  vc.id as vc_id,
  ci.id as ci_id,
  ci.store,
  max(case when sp.periodicity = 'month' and sp.period = 1 then sp.price end) AS "one_price",
  max(case when sp.periodicity = 'month' and sp.period = 1 then sp.previous_price end) AS "one_previous_price",
  max(case when sp.periodicity = 'month' and sp.period = 3 then sp.price end) AS "three_price",
  max(case when sp.periodicity = 'month' and sp.period = 3 then sp.previous_price end) AS "three_previous_price",
  max(case when sp.periodicity = 'month' and sp.period = 6 then sp.price end) AS "six_price",
  max(case when sp.periodicity = 'month' and sp.period = 6 then sp.previous_price end) AS "six_previous_price",
  max(case when sp.periodicity = 'month' and sp.period = 9 then sp.price end) AS "nine_price",
  max(case when sp.periodicity = 'month' and sp.period = 9 then sp.previous_price end) AS "nine_previous_price"
from subscription_packs sp 
join catalog_items ci on sp.catalog_id = ci.id 
join vehicle_classifications vc on ci.vehicle_classification_id = vc.id
group by
	sp.catalog_id,
	vc.make,
	vc.model,
	vc."version",
	vc.id,
	ci.id,
	ci.store,
	ci.daily_price,
	ci.weekly_price
;
"""

mock_query_response = dict(
  make='',
  model='',
  version='',
  vc_id='',
  ci_id='',
  store='',
  daily_price='',
  weekly_price='',
  one_price='',
  one_previous_price='',
  three_price='',
  three_previous_price='',
  six_price='',
  six_previous_price='',
  nine_price='',
  nine_previous_price='',
)

def serialized_data(elm = mock_query_response):
  return {
    'Classfication - company code': None,
    'Classfication Brand (Manufacturer)': elm.get('make'),
    'Classfication Family': elm.get('make'),
    'Classfication Model': elm.get('model'),
    'Classfication Year': None,
    'Classfication Version': elm.get('version'),
    'astaramove classficationid': elm.get('vc_id'),
    'astara move catalogID': elm.get('ci_id'),
    'Store': elm.get('store'),
    'price per day (without VAT)': None,
    'price per week (without VAT)': None,
    'price 1 month period (no VAT)': elm.get('one_price'),
    'price 1 month  Previous (no VAT)': elm.get('one_previous_price'),
    'price 3 month period (no VAT)': elm.get('three_price'),
    'price 3 month  Previous (no VAT)': elm.get('three_previous_price'),
    'price 6 month period (no VAT)': elm.get('six_price'),
    'price6 month  Previous (no VAT)': elm.get('six_previous_price'),
    'price 9 month period (no VAT)': elm.get('nine_price'),
    'price9 month  Previous (no VAT)': elm.get('nine_previous_price'),
  }
