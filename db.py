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
# INIT DB
# =========================
def init_db():
    conn = get_connection()
    c = conn.cursor()

    # USERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
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
# ADD USER
# =========================
def add_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except:
        return False

# =========================
# CHECK LOGIN
# =========================
def check_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    return c.fetchone() is not None

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
        confidence,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

# =========================
# GET HISTORY
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
