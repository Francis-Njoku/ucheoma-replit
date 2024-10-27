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

def drop_users_table():
    conn = get_db_connection()
    with conn.cursor() as cur:
        # Drop the transactions table first due to foreign key constraint
        cur.execute("DROP TABLE IF EXISTS transactions")
        # Then drop the users table
        cur.execute("DROP TABLE IF EXISTS users")
        conn.commit()
    conn.close()

def init_db():
    conn = get_db_connection()
    # Drop existing tables first
    drop_users_table()
    
    from models.user import User
    from models.transaction import Transaction
    
    User.create_table(conn)
    Transaction.create_table(conn)
    conn.close()
