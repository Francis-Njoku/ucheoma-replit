import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(
        host=os.environ['PGHOST'],
        database=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD'],
        port=os.environ['PGPORT']
    )

def init_db():
    conn = get_db_connection()
    from models.user import User
    from models.transaction import Transaction
    
    User.create_table(conn)
    Transaction.create_table(conn)
    conn.close()
