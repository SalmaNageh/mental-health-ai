import sqlite3

DB_NAME = "app.db"

# =========================
# CONNECT
# =========================
def get_connection():
    return sqlite3.connect(DB_NAME)


# =========================
# CREATE TABLES
# =========================
def init_db():

    conn = get_connection()
    c = conn.cursor()

    # users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================
# ADD USER
# =========================
def add_user(username, password):

    conn = get_connection()
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


# =========================
# CHECK LOGIN
# =========================
def check_user(username, password):

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = c.fetchone()
    conn.close()

    return user