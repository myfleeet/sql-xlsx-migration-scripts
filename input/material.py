output_file = 'Astara Move - Materials'

query = """
select s.cif, vc.make, vc.model, vc."version" 
from suppliers s, vehicles v, vehicle_classifications vc 
where s.id = v.supplier_id and vc.id = v.vehicle_classification_id
; 
"""

mock_query_response = dict(
  cif='',make='',model='',version=''
)

def serialized_data(elm = mock_query_response):
  return {
    # ok - FLET
    'company_code':'FLET',

    # ok - MAKEMODEL
    'comercial_model' : elm['make'].upper().replace(" ", "") + elm['model'].upper().replace(" ", ""),

    # ok - Z
    'type':'Z',

    # ok - VEHI
    'tipo_de_material':'VEHI',

    # ok - FESP
    'plant':'FESP',

    # ok - FLES
    'sales_organization':'FLES',

    # ok - 01
    'distribution_channel':None,

    # ok - MAKE MODEL VERSION
    'description' : elm['make'] + ' ' + elm['model'] + ' ' + elm['version'] if (elm['make'] and elm['model'] and elm['version']) else elm['make'] + ' ' + elm['model'],

    # ok - UN
    'measure_unit':'UN',

    'group_article':'ZMOD_VEH',

    'brand':'AM',

    'hierarchy':'0KIACVEHICVLIGVH0A',

    'position_type':'VMS0',

    'fixed_indicator':'X',

    'fiscal_classification':1,

    # ok - ES
    'country_of_origin' : 'ES',

    'posting_group':'01',
    
    'profit_Center':None,

    'rappel_group':'K0',

    'indicator':'X', 

    'valuation_class':'ZVN0',

    'indicator1':'X',

    'organizacion_de_compras':'FLES',

    # ok - CIF
    'vendor_code' : elm['cif'],

    # ok - 1
    'purchase_price' : 1,

    # EUR
    'currency' : 'EUR',

    'family':None,

    'empty' : None,

    # ES
    'specific_country_of_origin_inforecord':'ES',
  }