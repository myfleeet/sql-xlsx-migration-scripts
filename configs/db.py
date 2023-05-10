import configs.settings as settings
import psycopg2
import contextlib
import psycopg2.extras
from psycopg2.extensions import make_dsn

# DB connection
@contextlib.contextmanager
def get_db_connection(env):
  url = make_dsn(**settings.DB.get(env))
  conn = psycopg2.connect(url)
  try:
    yield conn
  finally:
    conn.close()
