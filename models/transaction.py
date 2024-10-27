from datetime import datetime
from dataclasses import dataclass

@dataclass
class Transaction:
    id: int
    user_id: int
    amount: float
    category: str
    description: str
    date: datetime
    transaction_type: str  # 'income' or 'expense'

    @staticmethod
    def create_table(conn):
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    amount DECIMAL(10,2) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    description TEXT,
                    date TIMESTAMP NOT NULL,
                    transaction_type VARCHAR(50) NOT NULL
                )
            """)
            conn.commit()
