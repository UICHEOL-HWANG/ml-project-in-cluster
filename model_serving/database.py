import psycopg2
from psycopg2.extras import RealDictCursor

def get_db():
    connection = psycopg2.connect(
        user="targetuser",
        password="targetpassword",
        host="target-postgres-server",
        port=5432,
        database="targetdatabase",
    )
    return connection