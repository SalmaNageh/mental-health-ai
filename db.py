import sqlite3
import hashlib
from datetime import datetime

# =========================
# CONNECT DB
# =========================
def get_connection():
    conn = sqlite3.connect("mindcare.db", check_same_thread=False)
    return conn

# =========================
# INIT DB (UPGRADED)
# =========================
def init_db():
    conn = get_connection()
    c = conn.cursor()

    # USERS TABLE (ADD ROLE)
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user'
    )
    """)

    # HISTORY TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        text TEXT,
        prediction TEXT,
        confidence REAL,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

# =========================
# HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# CREATE DEFAULT ADMIN (IMPORTANT)
# =========================
def create_admin():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES (?, ?, ?)
    """, ("admin", hash_password("admin123"), "admin"))

    conn.commit()
    conn.close()

# =========================
# ADD USER
# =========================
def add_user(username, password, role="user"):
    conn = get_connection()
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, hash_password(password), role))

        conn.commit()
        return True

    except:
        return False

# =========================
# CHECK USER (RETURN ROLE)
# =========================
def check_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT username, role
        FROM users
        WHERE username=? AND password=?
    """, (username, hash_password(password)))

    return c.fetchone()

# =========================
# ADD HISTORY
# =========================
def add_history(username, text, prediction, confidence):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO history (username, text, prediction, confidence, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        text,
        prediction,
        float(confidence),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

# =========================
# GET USER HISTORY
# =========================
def get_history(username):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT prediction, confidence, created_at
        FROM history
        WHERE username=?
        ORDER BY id DESC
    """, (username,))

    return c.fetchall()

# =========================
# GET ALL HISTORY (ADMIN)
# =========================
def get_all_history():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT * FROM history
        ORDER BY id DESC
    """)

    return c.fetchall()

# =========================
# GET ALL USERS (ADMIN)
# =========================
def get_all_users():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT id, username, role FROM users")

    return c.fetchall()

# =========================
# DELETE USER (ADMIN CONTROL)
# =========================
def delete_user(username):
    conn = get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE username=?", (username,))

    conn.commit()
    conn.close()
