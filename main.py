# DB
import configs.settings as settings
import psycopg2
import psycopg2.extras
from configs.db import get_db_connection
from configs.scaffolder import create_folder, define_folder_project_name

# Excel
import openpyxl

# utils
import logging
import os
import importlib


# Files
tables = [
  importlib.import_module(f"input.{file[:-3]}")
  for file in os.listdir("input")
  if file.endswith(".py")
]

# Query and Excel
def main():
  print('🚀')
  try:
    # For each ENV
    for env in list(settings.DB.keys()):
      with get_db_connection(env) as conn:
        
        # For each file
        for table in tables:
          with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            
            # Handle Errors in invalid file format
            if (
              not hasattr(table, 'query') or
              not hasattr(table, 'serialized_data') or
              not hasattr(table, 'output_file')
            ):
              raise Exception(f"\n\n[invalid format in file {table.__name__}]:\nshould contain query, serialized_data, output_file variables\n\n")
            
            # Execute query
            cursor.execute(table.query)
            sql_data = cursor.fetchall()
            
            # Write the excel file
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(list(table.serialized_data().keys()))
            for elm in sql_data:
              ws.append(list(table.serialized_data(elm).values()))

            project = define_folder_project_name(table.__name__.replace('input.', ''))
            wb.save(f"out/{project}/{env}/{table.output_file}.xlsx")

            # Log success
            print(f"✔ [{env}] - [{project}] - {table.output_file}.xlsx")
    print('✅')
  except Exception as e:
    logging.critical(e, exc_info=True)

if __name__ == "__main__":
  create_folder()
  main()