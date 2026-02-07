"""
Account Manager
Manages bot accounts, credentials, and profiles
Supports both SQLite (local) and Supabase (cloud) backends
"""

import sqlite3
import random
import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helper_functions import generate_random_email, generate_random_name, generate_random_phone, generate_random_address

try:
    from src.supabase_client import get_supabase_manager
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

logger = logging.getLogger(__name__)

DB_FILE = "database/userdata.db"


class AccountManager:
    """Manage user accounts for bot operations"""

    def __init__(self, db_file=None, use_supabase=None):
        self.db_file = db_file or DB_FILE
        self.use_supabase = use_supabase if use_supabase is not None else SUPABASE_AVAILABLE

        if self.use_supabase:
            self.supabase = get_supabase_manager()
            if not self.supabase.is_connected():
                logger.warning("Supabase not available, falling back to SQLite")
                self.use_supabase = False

        if not self.use_supabase:
            self._ensure_db()

    def _ensure_db(self):
        """Ensure SQLite database exists"""
        if not os.path.exists(self.db_file):
            logger.warning(f"Database not found: {self.db_file}")
            logger.info("Run 'python database/init_db.py' to initialize database")

    def create_account(
        self,
        platform: str,
        email: Optional[str] = None,
        password: str = "SecurePassword123!",
        username: Optional[str] = None,
        account_name: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[str]:
        """Create a new account"""

        if not email:
            email = generate_random_email()

        if self.use_supabase:
            return self.supabase.create_account(
                platform=platform,
                email=email,
                password_encrypted=password,
                username=username,
                account_name=account_name,
                notes=notes,
            )
        else:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

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
                return str(account_id)

            except sqlite3.IntegrityError:
                logger.error(f"Account already exists: {email}")
                return None
            finally:
                conn.close()

    def get_account(self, platform: str, account_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get account by platform or ID"""

        if account_id:
            if self.use_supabase:
                return self.supabase.get_account(account_id)
            else:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
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
        else:
            if self.use_supabase:
                accounts = self.supabase.get_accounts_by_platform(platform)
                return random.choice(accounts) if accounts else None
            else:
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM accounts
                    WHERE platform = ? AND status = 'active'
                    ORDER BY RANDOM() LIMIT 1
                """, (platform,))
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

    def get_random_account(self, platform: str) -> Optional[Dict[str, Any]]:
        """Get a random active account for platform"""
        return self.get_account(platform)

    def get_all_accounts(self, platform: str) -> List[Dict[str, Any]]:
        """Get all accounts for a platform"""
        if self.use_supabase:
            return self.supabase.get_accounts_by_platform(platform)
        else:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM accounts
                WHERE platform = ? AND status = 'active'
            """, (platform,))
            rows = cursor.fetchall()
            conn.close()

            return [
                {
                    "id": row[0],
                    "platform": row[1],
                    "email": row[2],
                    "password": row[3],
                    "first_name": row[4],
                    "last_name": row[5],
                    "phone": row[6]
                }
                for row in rows
            ]

    def update_last_used(self, account_id: str) -> bool:
        """Update last used timestamp"""
        if self.use_supabase:
            return self.supabase.update_account_usage(account_id)
        else:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE accounts
                SET last_used = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (account_id,))
            conn.commit()
            conn.close()
            return True

    def update_account_stats(self, account_id: str, success: bool) -> bool:
        """Update account success/failure stats"""
        if self.use_supabase:
            return self.supabase.update_account_stats(account_id, success)
        else:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            if success:
                cursor.execute("""
                    UPDATE accounts
                    SET success_count = success_count + 1
                    WHERE id = ?
                """, (account_id,))
            else:
                cursor.execute("""
                    UPDATE accounts
                    SET failure_count = failure_count + 1
                    WHERE id = ?
                """, (account_id,))

            conn.commit()
            conn.close()
            return True

    def deactivate_account(self, account_id: str) -> bool:
        """Deactivate an account"""
        if self.use_supabase:
            return self.supabase.client.table("accounts").update({"status": "inactive"}).eq("id", account_id).execute()
        else:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("UPDATE accounts SET status = 'inactive' WHERE id = ?", (account_id,))
            conn.commit()
            conn.close()

            logger.info(f"Deactivated account ID: {account_id}")
            return True

# Singleton
_account_manager = None

def get_account_manager():
    """Get account manager instance"""
    global _account_manager
    if _account_manager is None:
        _account_manager = AccountManager()
    return _account_manager
