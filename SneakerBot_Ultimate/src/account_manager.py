import random
import string
import sqlite3
from utils.helper_functions import generate_random_email

DB_FILE = "database/userdata.db"


def create_account(platform, password="SecurePassword123!"):
    """Creates an account and stores it in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    email = generate_random_email()

    cursor.execute("""
        INSERT INTO accounts (platform, email, password) VALUES (?, ?, ?)
    """, (platform, email, password))

    conn.commit()
    conn.close()

    print(f"✅ Created {platform} account: {email}")
    return email, password

