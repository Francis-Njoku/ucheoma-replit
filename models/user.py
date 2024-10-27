from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    email: str
    password_hash: str
    subscription_type: str  # 'basic' or 'premium'
    subscription_status: str
    created_at: datetime
    stripe_customer_id: Optional[str] = None
    email_verified: bool = False
    verification_token: Optional[str] = None

    @staticmethod
    def create_table(conn):
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    subscription_type VARCHAR(50) NOT NULL,
                    subscription_status VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    stripe_customer_id VARCHAR(255),
                    email_verified BOOLEAN DEFAULT FALSE,
                    verification_token VARCHAR(255)
                )
            """)
            conn.commit()
