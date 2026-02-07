"""
Account Manager
Manages bot accounts, credentials, and profiles
"""

import sqlite3
import random
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helper_functions import generate_random_email, generate_random_name, generate_random_phone, generate_random_address
from utils.logger import logger

DB_FILE = "database/userdata.db"

class AccountManager:
    """Manage user accounts for bot operations"""
    
    def __init__(self, db_file=None):
        self.db_file = db_file or DB_FILE
        self._ensure_db()
    
    def _ensure_db(self):
        """Ensure database exists"""
        if not os.path.exists(self.db_file):
            logger.warning(f"Database not found: {self.db_file}")
            logger.info("Run 'python database/init_db.py' to initialize database")
    
    def create_account(self, platform, email=None, password="SecurePassword123!"):
        """Create a new account"""
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        if not email:
            email = generate_random_email()
        
        name = generate_random_name()
        phone = generate_random_phone()
        
        try:
            cursor.execute("""
                INSERT INTO accounts (platform, email, password, first_name, last_name, phone)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (platform, email, password, name["first_name"], name["last_name"], phone))
            
            conn.commit()
            account_id = cursor.lastrowid
            
            logger.info(f"✅ Created account: {email} for {platform}")
            return account_id
            
        except sqlite3.IntegrityError:
            logger.error(f"Account already exists: {email}")
            return None
        finally:
            conn.close()
    
    def get_account(self, platform, account_id=None):
        """Get account by platform"""
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        if account_id:
            cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        else:
            cursor.execute("SELECT * FROM accounts WHERE platform = ? AND status = 'active' ORDER BY RANDOM() LIMIT 1", (platform,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "platform": row[1],
                "email": row[2],
                "password": row[3],
                "first_name": row[4],
                "last_name": row[5],
                "phone": row[6]
            }
        return None
    
    def get_random_account(self, platform):
        """Get a random active account for platform"""
        return self.get_account(platform)
    
    def update_last_used(self, account_id):
        """Update last used timestamp"""
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE accounts SET last_used = CURRENT_TIMESTAMP WHERE id = ?", (account_id,))
        conn.commit()
        conn.close()
    
    def deactivate_account(self, account_id):
        """Deactivate an account"""
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE accounts SET status = 'inactive' WHERE id = ?", (account_id,))
        conn.commit()
        conn.close()
        
        logger.info(f"Deactivated account ID: {account_id}")

# Singleton
_account_manager = None

def get_account_manager():
    """Get account manager instance"""
    global _account_manager
    if _account_manager is None:
        _account_manager = AccountManager()
    return _account_manager
