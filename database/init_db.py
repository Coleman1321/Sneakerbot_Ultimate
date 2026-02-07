"""
Database Initialization Script
Creates all necessary tables for the SneakerBot Ultimate project
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = "database/userdata.db"

def init_database():
    """Initialize all database tables"""
    
    # Ensure database directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # ====================================
    # Accounts Table
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP,
            status TEXT DEFAULT 'active',
            UNIQUE(platform, email)
        )
    """)
    
    # ====================================
    # Payment Information Table
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payment_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            card_number TEXT NOT NULL,
            card_holder TEXT NOT NULL,
            expiry_month TEXT NOT NULL,
            expiry_year TEXT NOT NULL,
            cvv TEXT NOT NULL,
            billing_address TEXT,
            billing_city TEXT,
            billing_state TEXT,
            billing_zip TEXT,
            billing_country TEXT DEFAULT 'US',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    """)
    
    # ====================================
    # Shipping Addresses Table
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipping_addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            address_line1 TEXT NOT NULL,
            address_line2 TEXT,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            country TEXT DEFAULT 'US',
            phone TEXT,
            is_default BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    """)
    
    # ====================================
    # Proxies Table
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proxies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proxy_url TEXT NOT NULL UNIQUE,
            proxy_type TEXT DEFAULT 'http',
            username TEXT,
            password TEXT,
            is_active BOOLEAN DEFAULT 1,
            success_count INTEGER DEFAULT 0,
            failure_count INTEGER DEFAULT 0,
            last_used TIMESTAMP,
            response_time REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # ====================================
    # Tasks Table (for tracking bot runs)
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            sneaker_id TEXT,
            sneaker_name TEXT,
            size TEXT,
            account_id INTEGER,
            proxy_id INTEGER,
            status TEXT DEFAULT 'pending',
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            error_message TEXT,
            success BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id),
            FOREIGN KEY (proxy_id) REFERENCES proxies(id)
        )
    """)
    
    # ====================================
    # Raffle Entries Table
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raffle_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            sneaker_id TEXT NOT NULL,
            sneaker_name TEXT,
            size TEXT NOT NULL,
            email TEXT NOT NULL,
            account_id INTEGER,
            entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'entered',
            result TEXT,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    """)
    
    # ====================================
    # Stock Monitoring Table
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_monitoring (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            sneaker_id TEXT NOT NULL,
            sneaker_name TEXT,
            target_size TEXT,
            in_stock BOOLEAN DEFAULT 0,
            last_checked TIMESTAMP,
            notification_sent BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(platform, sneaker_id, target_size)
        )
    """)
    
    # ====================================
    # Successful Purchases Table
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            sneaker_name TEXT NOT NULL,
            size TEXT,
            price REAL,
            account_id INTEGER,
            order_number TEXT,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            screenshot_path TEXT,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    """)
    
    # ====================================
    # Bot Performance Metrics Table
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            task_id INTEGER,
            metric_type TEXT NOT NULL,
            metric_value REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    """)
    
    # ====================================
    # CAPTCHA Solutions Table
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS captcha_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            captcha_type TEXT NOT NULL,
            site_key TEXT,
            solution_time REAL,
            success BOOLEAN DEFAULT 0,
            cost REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    """)
    
    # ====================================
    # Configuration History Table
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS config_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            config_key TEXT NOT NULL,
            config_value TEXT,
            changed_by TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # ====================================
    # Error Logs Table
    # ====================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            error_type TEXT,
            error_message TEXT,
            stack_trace TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    """)
    
    conn.commit()
    
    # Create indexes for better query performance
    create_indexes(cursor)
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully!")
    print(f"📁 Database location: {os.path.abspath(DB_PATH)}")


def create_indexes(cursor):
    """Create database indexes for performance optimization"""
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_accounts_platform ON accounts(platform)",
        "CREATE INDEX IF NOT EXISTS idx_accounts_email ON accounts(email)",
        "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)",
        "CREATE INDEX IF NOT EXISTS idx_tasks_platform ON tasks(platform)",
        "CREATE INDEX IF NOT EXISTS idx_proxies_active ON proxies(is_active)",
        "CREATE INDEX IF NOT EXISTS idx_raffle_entries_site ON raffle_entries(site)",
        "CREATE INDEX IF NOT EXISTS idx_stock_monitoring_platform ON stock_monitoring(platform)",
        "CREATE INDEX IF NOT EXISTS idx_purchases_platform ON purchases(platform)",
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)


def add_sample_data():
    """Add sample data for testing (optional)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Sample account
    cursor.execute("""
        INSERT OR IGNORE INTO accounts (platform, email, password, first_name, last_name, phone)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("Nike", "test@example.com", "SecurePassword123!", "John", "Doe", "555-0123"))
    
    # Sample proxy
    cursor.execute("""
        INSERT OR IGNORE INTO proxies (proxy_url, proxy_type)
        VALUES (?, ?)
    """, ("http://proxy1.example.com:8080", "http"))
    
    conn.commit()
    conn.close()
    print("✅ Sample data added!")


def reset_database():
    """Delete and reinitialize the database (use with caution!)"""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️  Old database deleted")
    init_database()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        init_database()
    
    # Optionally add sample data
    if len(sys.argv) > 1 and sys.argv[1] == "--sample":
        add_sample_data()
