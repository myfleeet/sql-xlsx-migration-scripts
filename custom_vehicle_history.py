# DB
import time
import utils.utils as utils
import configs.settings as settings
import psycopg2
import psycopg2.extras
from configs.db import get_db_connection
from configs.scaffolder import create_folder, define_folder_project_name, folders

# Excel
import openpyxl

# utils
import logging

"""
GLOBALS
"""

# 🟧 Update file name 
output_file = "Vehicle History"
global_folder = 'goto'

"""
HELPER FUNCTION
"""


def check_incidence_counter(elm):
    if len(elm.get("incidences_1")) != 0:
        return len(elm.get("incidences_1"))
    incidences = 0
    if elm.get("incidences_2") is not None:
        for incident in list(elm.get("incidences_2")):
            if incident.get("checks") is not None:
                for check in incident.get("checks"):
                    if check.get("incidence_severity") is not None:
                        incidences = incidences + 1
    return incidences


"""
SERIALIZER
"""

# schema
# https://logistics.astaramove.com/vehicles/d1554884-fca4-4056-b161-f3f512021bd4/history
serialized_data = {
    "VIN": None,
    "Move Internal Vehicle ID": None,
    "Action Date": None,
    "Action Description": None,
    "Action Type": None,
    "Action link (id) for Action": None,
}


def checks_serialized_data(elm):
    return {
        "VIN": elm.get("vin"),
        "Move Internal Vehicle ID": elm.get("vehicle_id"),
        "Action Date": utils.to_utc_iso_string(elm.get("date")),
        "Action Description": utils.json_to_str(dict(
            check_report_id=elm.get("check_report_id"),
            checked_at=elm.get("checked_at"),
            date=utils.to_utc_iso_string(elm.get("date")),
            incidence_count=check_incidence_counter(elm),
            report_check_type=elm.get("report_check_type"),
            type=elm.get("type"),
        )),
        "Action Type": elm.get("type"),
        "Action link (id) for Action": elm.get("vehicle_id"),
    }


def subscription_serialized_data(elm):
    return {
        "VIN": elm.get("vin"),
        "Move Internal Vehicle ID": elm.get("vehicle_id"),
        "Action Date": utils.to_utc_iso_string(elm.get("date")),
        "Action Description": utils.json_to_str(dict(
            client_id=elm.get("client_id"),
            date=utils.to_utc_iso_string(elm.get("date")),
            delivered_to_client=elm.get("delivered_to_client"),
            delivery_at=utils.to_utc_iso_string(elm.get("delivery_at")),
            delivery_document=elm.get("delivery_document"),
            delivery_is_external=elm.get("delivery_is_external"),
            finished_at=utils.to_utc_iso_string(elm.get("finished_at")),
            periodicity=elm.get("periodicity"),
            pick_up_at=utils.to_utc_iso_string(elm.get("pick_up_at")),
            pick_up_document=elm.get("pick_up_document"),
            pick_up_is_external=elm.get("pick_up_is_external"),
            picked_up_from_client=elm.get("picked_up_from_client"),
            started_at=utils.to_utc_iso_string(elm.get("started_at")),
            subscription_id=elm.get("subscription_id"),
            type=elm.get("type"),
            vehicle_assignment_id=elm.get("vehicle_assignment_id"),
        )),
        "Action Type": elm.get("type"),
        "Action link (id) for Action": elm.get("vehicle_id"),
    }


def registration_serialized_data(elm):
    return {
        "VIN": elm.get("vin"),
        "Move Internal Vehicle ID": elm.get("vehicle_id"),
        "Action Date": utils.to_utc_iso_string(elm.get("date")),
        "Action Description": utils.json_to_str(dict(
            date=utils.to_utc_iso_string(elm.get("date")),
            supplier_id=elm.get("supplier_id"),
            type=elm.get("type"),
        )),
        "Action Type": elm.get("type"),
        "Action link (id) for Action": elm.get("vehicle_id"),
    }


def supplier_return_serialized_data(elm):
    return {
        "VIN": elm.get("vin"),
        "Move Internal Vehicle ID": elm.get("vehicle_id"),
        "Action Date": utils.to_utc_iso_string(elm.get("date")),
        "Action Description": utils.json_to_str(dict(
            date=utils.to_utc_iso_string(elm.get("date")),
            supplier_id=elm.get("supplier_id"),
            type=elm.get("type"),
        )),
        "Action Type": elm.get("type"),
        "Action link (id) for Action": elm.get("vehicle_id"),
    }

"""
QUERY
"""

query = dict(
    get_all_ids="""
      select v.id, v.vin 
      from vehicles v 
    """,
    get_by_id=dict(
        checks=dict(
            query="""
            select
              'check' as type,
              v.vin,
              cr.vehicle_id,
              cr.created_at as date,
              cr.report ->> 'meta' as checked_at,
              cr.id as check_report_id,
              cr.incidences as incidences_1,
              cr.report -> 'check_groups' as incidences_2, -- for each "check_group", return "checks" , for each "incidence_severity" not NULL
              cr.report ->> 'check_type' as report_check_type
            from check_reports cr
            join vehicles v on v.id = cr.vehicle_id
            where
                cr.vehicle_id = '{id}' and
                v.vin = '{vin}'
            ;
            """,
            serialized_data=checks_serialized_data,
        ),
        subscriptions=dict(
            query="""
            select
              va.vehicle_id,
              v.vin,
              'subscription' as type,
              s.created_at as date,
              va.delivery_at as started_at,
              va.pick_up_at as finished_at,
              s.periodicity,
              s.client_id,
              s.id as subscription_id,
              va.id as vehicle_assignment_id,
              va.picked_up_from_client,
              va.delivery_document,
              va.pick_up_document,
              va.delivery_is_external,
              va.pick_up_is_external,
              va.delivery_at,
              va.pick_up_at,
              va.unassigned_at ,
              va.delivered_to_client
            from subscriptions s
            join vehicle_assignments va on s.id = va.subscription_id
            join vehicles v on v.id = va.vehicle_id
            where
              va.vehicle_id = '{id}' and
              v.vin = '{vin}' and
              ((va.unassigned_at is not null and va.delivered_to_client = 'true') or
              va.unassigned_at is null)
            ;
            """,
            serialized_data=subscription_serialized_data,
        ),
        registrations=dict(
            query="""
            select 
              'registration' as type,
              v.vin, 
              v.id as vehicle_id,
              v.received_at as date,
              v.supplier_id as supplier_id
            from vehicles v 
            where 
                v.id = '{id}' and
                v.vin = '{vin}'
            ;
            """,
            serialized_data=registration_serialized_data,
        ),
        supplier_returns=dict(
            query="""
            select
              'supplier_return' as type,
              v.vin,
              v.id as vehicle_id,
              v.returned_real_at as date,
              v.supplier_id as supplier_id
            from vehicles v
            where
                v.id = '{id}' and
                v.vin = '{vin}'
            ;
            """,
            serialized_data=supplier_return_serialized_data,
        ),
    ),
)


# Query and Excel
def high_hopes():
    print("🚀")
    start_time = time.time()
    try:
        for env in list(settings.DB.keys()):
            with get_db_connection(env) as conn:
                with conn.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor
                ) as cursor:
                    # Execute query
                    cursor.execute(query.get("get_all_ids"))
                    sql_data = cursor.fetchall()

                    # Write the excel file
                    wb = openpyxl.Workbook()
                    ws = wb.active
                    ws.append(list(serialized_data.keys()))

                    # For each ID execute all the queries
                    for idx, sql_data_elm in enumerate(sql_data):
                        
                        # For each required table execute the Query
                        for key in query.get("get_by_id").keys():
                            sql_query = (
                                query.get("get_by_id")
                                .get(key)
                                .get("query")
                                .format(
                                    id=sql_data_elm.get("id"),
                                    vin=sql_data_elm.get("vin"),
                                )
                            )
                            cursor.execute(sql_query)
                            request = cursor.fetchall()

                            # Serialize each valid response into a row
                            for res in request:
                                col = query["get_by_id"][key]["serialized_data"](res)
                                ws.append(list(col.values()))

                        print(f"✔ [{env}] - {idx + 1} / {len(sql_data)}")

                    # Define the output file name
                    project = define_folder_project_name(folders.get(global_folder))
                    wb.save(f"out/{project}/{env}/{output_file}.xlsx")
                    print(f"✔ [{env}] - [{project}] - {output_file}.xlsx")
        
        # Print the total time
        total_time = round(time.time() - start_time, 2)
        print(f"🏁 {total_time} seconds - {total_time / 60} minutes")
        print("✅")
    except Exception as e:
        logging.critical(e, exc_info=True)


create_folder()
high_hopes()
