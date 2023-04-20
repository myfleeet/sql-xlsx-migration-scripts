import psycopg2
import psycopg2.extras
from psycopg2.extensions import make_dsn
import openpyxl
import settings
import logging

# from input.material import query, serialized_data, output_file
from input.classifications import query, serialized_data, output_file

url = make_dsn(**settings.DB)
conn = psycopg2.connect(url)

def main():
  try:
    with conn:
      with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute(query)
        sql_data = cursor.fetchall()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(list(serialized_data().keys()))
        for elm in sql_data:
          ws.append(list(serialized_data(elm).values()))
        wb.save(f"{output_file}.xlsx")
  except Exception as e:
    logging.critical(e, exc_info=True)
  finally:
    conn.close()

if __name__ == "__main__":
  main()