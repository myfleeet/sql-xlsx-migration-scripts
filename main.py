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
def get_db_connection():
  url = make_dsn(**settings.DB)
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

# Query and Excel
def main():
  try:
    with get_db_connection() as conn:
      for table in tables:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
          cursor.execute(table.query)
          sql_data = cursor.fetchall()
          wb = openpyxl.Workbook()
          ws = wb.active
          ws.append(list(table.serialized_data().keys()))
          for elm in sql_data:
            ws.append(list(table.serialized_data(elm).values()))
          wb.save(f"out/{table.output_file}.xlsx")
  except Exception as e:
    logging.critical(e, exc_info=True)

if __name__ == "__main__":
  main()