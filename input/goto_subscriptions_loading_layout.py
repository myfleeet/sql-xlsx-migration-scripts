import utils.utils as utils

output_file = "Subscription Loading Layout"

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
	pd.tax_rate, -- % percentage
	c2.code,
	c2.amount_off,
	c2.percent_off,
	c2.duration, -- once (1 month) | foverer (all)
	s.attached_documents,
 	s.comment
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
    sub_id="",
    client_id="",
    status="",
    make="",
    model="",
    version="",
    color="",
    vin="",
    delivery_address="",
    delivery_at="",
    delivery_note="",
    cancel_requested_at="",
    pick_up_address="",
    pick_up_at="",
    insurance_by="",
    insurance_cost="",
    method_type="",
    failed_scoring="",
    base_amount="",
    subscription_pack_period="",
    subscription_pack_price="",
    code="",
    amount_off="",
    percent_off="",
    attached_documents="",
    tax_rate="",
    duration="",
)


def taxify(elm, value):
    return f"{value} * {elm.get('tax_rate')}%"

def get_cuota_actual(elm):
    # if no discount
    if not elm.get("code"):
      return {
          "1": f"{utils.get_price(elm)} + {elm.get('tax_rate')}",
          "2": f"{utils.get_price(elm)} + {elm.get('tax_rate')}",
      }
        
    # if discount
    if elm.get("duration") == "once":
        if elm.get("amount_off"):
            return {
                "1": f"{utils.get_price(elm)} + {elm.get('tax_rate')} + {elm.get('amount_off')} €",
                "2": f"{utils.get_price(elm)} + {elm.get('tax_rate')}",
            }
        if elm.get("percent_off"):
            return {
                "1": f"{utils.get_price(elm)} + {elm.get('tax_rate')} + {elm.get('percent_off')} %",
                "2": f"{utils.get_price(elm)} + {elm.get('tax_rate')}",
            }
    if elm.get("duration") == "forever":
        if elm.get("amount_off"):
            return {
                "1": None,
                "2": f"{utils.get_price(elm)} + {elm.get('tax_rate')} + {elm.get('amount_off')} €",
            }
        if elm.get("percent_off"):
            return {
                "1": None,
                "2": f"{utils.get_price(elm)} + {elm.get('tax_rate')} + {elm.get('percent_off')} %",
            }



# ✅ OK
def get_subtotal_plus_discount(elm):
    # if not discount
    if not elm.get("code"):
      return utils.get_price(elm)
    # if discount
    if elm.get("amount_off"):
        return utils.get_price(elm) - elm.get('amount_off')
    if elm.get("percent_off"):
        return utils.get_price(elm) - (utils.get_price(elm) * (elm.get('percent_off') / 100))
    

# ✅ OK
def get_tax_rate(elm):
    if(elm.get('tax_rate')):
      return get_subtotal_plus_discount(elm) * elm.get('tax_rate')


def serialized_data(elm=mock_query_response):
    return {
        # 'SubscriptionMoveId': elm.get('sub_id'),
        # 'SubscriptionSFDCId': None,
        # 'CustomerMoveId': elm.get('client_id'),
        # 'CustomerSFDCId': None,
        # 'CompanyCode': None,
        # 'Status': elm.get('status'),
        # 'Substatus': None,
        # 'SubscriptionOrigin': None,
        # 'Brand': elm.get('make'),
        # 'family': utils.family_code(elm),
        # 'model': elm.get('model'),
        # 'version': elm.get('version'),
        # 'modelyear': None,
        # 'color': elm.get('color'),
        # 'upholstery': None,
        # 'VIN': elm.get('vin'),
        # 'deliveryType': utils.type_of_delivery(elm.get('delivery_address')),
        # 'deliveryDate': utils.time_format(elm.get('delivery_at')),
        # 'DeliveryHour': utils.hours_format(elm.get('delivery_at')),
        # 'DeliveryPickupaddress': utils.normalize_address(elm.get('delivery_address')),
        # 'DeliveryComments': elm.get('delivery_note'),
        # 'RequestReturnDate': elm.get('cancel_requested_at'),
        # 'PlannedReturnDate': elm.get('cancel_requested_at'),
        # 'returnDate': utils.time_format(elm.get('pick_up_at')),
        # 'returnHour': utils.hours_format(elm.get('pick_up_at')),
        # 'returnAddress': utils.normalize_address(elm.get('pick_up_address')),
        # 'ReturnType': utils.type_of_delivery(elm.get('pick_up_address')),
        # 'pickupDate': elm.get('pick_up_at'),
        # 'insurance': elm.get('insurance_by'),
        # 'paymentMethod': elm.get('method_type'),
        # 'EndingReason': None,
        # 'scoring': None,
        # 'ProbIncumplimientoScore': 'True' if elm.get('failed_scoring') else None,
        # 'Nota': None,
        # 'Decil': None,
        # 'Percentil': None,
        # 'deposit': None,
        # 'period': elm.get('subscription_pack_period') or 1,
        # 'extraInsuranceCost': elm.get('insurance_cost'), # EXTRA ?

        # Cuota actual                -> IF FOREVER -> subscriptionCost + IVA + descuento && IF ONCE -> subscriptionCost + IVA
        # Cuota primer mes            -> IF FOREVER -> None && ONCE -> subscriptionCost + IVA + descuento
        # Subtotal sin descuento      -> subscriptionCost - IVA
        # Subtotal con descuento      -> subscriptionCost - IVA + descuento
        # IVA                         -> ((subscriptionCost + descuento) * tax rate) / 100
        "PromoCode": elm.get("code"),
        "PromoDuration": elm.get("duration"),
        "PromoDisccount": utils.promo_discount(elm),                 # -> ✅ 🔥 [MAIN]

        "CuotaPrimerMes": get_cuota_actual(elm).get("1"),            # -> IF FOREVER -> None                                    && ONCE -> subscriptionCost + IVA + descuento
        "CuotaActual": get_cuota_actual(elm).get("2"),               # -> IF FOREVER -> subscriptionCost + IVA + descuento      && IF ONCE -> subscriptionCost + IVA
        "SubtotalSinDescuento": utils.get_price(elm),                # -> ✅ 🔥 [MAIN] subscriptionCost
        "SubtotalConDescuento": get_subtotal_plus_discount(elm),     # -> ✅ subscriptionCost + descuento
        "tax_rate": elm.get("tax_rate"),
        "IVA": get_tax_rate(elm),                                    # -> ✅ ((subscriptionCost + descuento) * tax rate) / 100


        # "Comments": elm.get("comment"),
        # "History Json": None,
        # "Current Contracts": utils.json_to_str(elm.get("attached_documents")),
    }
