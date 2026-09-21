"""
Database model dan helper sederhana menggunakan SQLite bawaan Python.
Tidak memerlukan dependensi ORM berat, ringan, dan siap pakai.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "database.sqlite")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Tabel Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Tabel Subscriptions / Transactions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT UNIQUE NOT NULL,
        user_email TEXT NOT NULL,
        plan_name TEXT NOT NULL,
        amount INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        payment_method TEXT,
        pakasir_payload TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def create_order(order_id, user_email, plan_name, amount):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO orders (order_id, user_email, plan_name, amount, status)
    VALUES (?, ?, ?, ?, 'pending')
    """, (order_id, user_email, plan_name, amount))
    conn.commit()
    conn.close()

def get_order(order_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def mark_order_completed(order_id, payment_method, payload_str):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    UPDATE orders
    SET status = 'completed',
        payment_method = ?,
        pakasir_payload = ?,
        completed_at = ?
    WHERE order_id = ?
    """, (payment_method, payload_str, now, order_id))
    conn.commit()
    conn.close()

def is_user_active(email):
    """Cek apakah user memiliki order completed (langganan aktif)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(*) as count FROM orders
    WHERE user_email = ? AND status = 'completed'
    """, (email,))
    row = cursor.fetchone()
    conn.close()
    return row["count"] > 0 if row else False
