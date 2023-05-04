# DB
import settings
import psycopg2
import contextlib
import psycopg2.extras
from psycopg2.extensions import make_dsn

# Excel
import openpyxl

# utils
import logging
import os
import importlib

# DB connection
@contextlib.contextmanager
def get_db_connection(env):
  url = make_dsn(**settings.DB.get(env))
  conn = psycopg2.connect(url)
  try:
    yield conn
  finally:
    conn.close()

# Files
tables = [
  importlib.import_module(f"input.{file[:-3]}")
  for file in os.listdir("input")
  if file.endswith(".py")
]

# create folder "out"
def create_folder():
  for folder in ['goto', 'accenture']:
    for env in list(settings.DB.keys()):
      os.makedirs(f'out/{folder}/{env}', exist_ok=True)

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
            cursor.execute(table.query)
            sql_data = cursor.fetchall()
            # Write Excel
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(list(table.serialized_data().keys()))
            for elm in sql_data:
              ws.append(list(table.serialized_data(elm).values()))
            project = 'goto' if (table.__name__.startswith('input.goto') or table.__name__.startswith('input._goto')) else 'accenture'
            wb.save(f"out/{project}/{env}/{table.output_file}.xlsx")
            print(f"✔ [{env}] - [{project}] - {table.output_file}.xlsx")
    print('✅')
  except Exception as e:
    logging.critical(e, exc_info=True)

if __name__ == "__main__":
  create_folder()
  main()