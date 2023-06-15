import utils.utils as utils

output_file = "Subscription documents"

query = """
select 
	s.id,
	s.status,
	vc.make,
	vc.model,
	vc."version",
	si.color,
	v.license_plate,
	v.vin,
	va.delivery_is_external,
	va.pick_up_is_external,
	va.delivery_document,
	va.pick_up_document,
	va.particular_terms_document 
from subscriptions s 
left join subscription_items si on s.id = si.subscription_id 
left join vehicle_classifications vc on vc.id = si.vehicle_classification_id 
left join vehicle_assignments va on s.id = va.subscription_id
left join vehicles v on v.id = va.vehicle_id 
; 
"""

mock_query_response = dict(
    id="",
    status="",
    make="",
    model="",
    version="",
    color="",
    license_plate="",
    vin="",
    delivery_is_external="",
    pick_up_is_external="",
    delivery_document="",
    pick_up_document="",
    particular_terms_document="",
)


def serialized_data(elm=mock_query_response):
    return {
        "SubscriptionMoveId": elm.get("id"),
        "SubscriptionSFDCId": None,
        "ISENDED": "true" if elm.get("status") == "ended" else None,
        "Brand": elm.get("make"),
        "family": utils.family_code(elm),
        "model": elm.get("model"),
        "version": elm.get("version"),
        "color": elm.get("color"),
        "license plater": elm.get("license_plate"),
        "VIN": elm.get("vin"),
        "delivery external": "true" if elm.get("delivery_is_external") else None,
        "pick up external": "true" if elm.get("pick_up_is_external") else None,
        "filePickUp": elm.get("pick_up_document"),
        "fileDelivery": elm.get("delivery_document"),
        "fileContract": elm.get("particular_terms_document"),
    }
