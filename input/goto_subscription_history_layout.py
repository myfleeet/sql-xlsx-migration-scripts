import utils.utils as utils

output_file = "Subscription History Layout"

query = """
select 
	s.id,
	vc.make,
	vc.model,
	vc."version",
	si.color,
	v.license_plate,
	v.vin,
	va.delivery_address,
	s.started_at,
	s.finished_at,
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
    make="",
    model="",
    version="",
    color="",
    license_plate="",
    vin="",
    delivery_address="",
    started_at="",
    finished_at="",
    particular_terms_document="",
)


def serialized_data(elm=mock_query_response):
    return {
        "SubscriptionMoveId": elm.get("id"),
        "SubscriptionSFDCId": None,
        "Brand": elm.get("make"),
        "family": utils.family_code(elm),
        "model": elm.get("model"),
        "version": elm.get("version"),
        "color": elm.get("color"),
        "license plater": elm.get("license_plate"),
        "VIN": elm.get("vin"),
        "deliveryType": utils.type_of_delivery(elm.get("delivery_address")),
        "StartDate": elm.get("started_at"),
        "EndDate": elm.get("finished_at"),
        "Contracts": elm.get("particular_terms_document"),
    }
