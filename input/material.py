import utils

output_file = 'Astara Move - Materials'

query = """
select 
  distinct s.cif, 
  trim(vc.model) as model, 
  vc.make, 
  vc."version"
from 
  suppliers s, 
  vehicles v, 
  vehicle_classifications vc 
where 
  s.id = v.supplier_id and 
  vc.id = v.vehicle_classification_id
order by
  model
;
"""

mock_query_response = dict(
  cif='',
  make='',
  model=''
)

def serialized_data(elm = mock_query_response):
  return {
    'company_code':'FLET',
    'comercial_model' : utils.commercial_model(elm),
    'type':'Z',
    'tipo_de_material':'VEHI',
    'plant':'FESP',
    'sales_organization':'FLES',
    'distribution_channel':None,
    'description' : utils.make_model(elm),
    'measure_unit':'UN',
    'group_article':'ZMOD_VEH',
    'brand':'AM',
    'hierarchy':'0KIACVEHICVLIGVH0A',
    'position_type':'VMS0',
    'fixed_indicator':'X',
    'fiscal_classification':1,
    'country_of_origin' : 'ES',
    'posting_group':'01',
    'profit_Center':None,
    'rappel_group':'K0',
    'indicator':'X', 
    'valuation_class':'ZVN0',
    'indicator1':'X',
    'organizacion_de_compras':'FLES',
    'vendor_code' : elm.get('cif'),
    'purchase_price' : 1,
    'currency' : 'EUR',
    'family': None,
    'empty' : None,
    'specific_country_of_origin_inforecord':'ES',
  }