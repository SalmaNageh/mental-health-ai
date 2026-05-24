import streamlit as st
import sqlite3
import pandas as pd

from db import get_connection

st.set_page_config(page_title="Admin Panel", layout="wide")

st.title("👑 Admin Dashboard")

# =========================
# CHECK ADMIN
# =========================
if st.session_state.get("role") != "admin":
    st.error("Access Denied ❌ Admins only")
    st.stop()

conn = get_connection()

# =========================
# LOAD DATA
# =========================
users = pd.read_sql_query("SELECT * FROM users", conn)
history = pd.read_sql_query("SELECT * FROM history", conn)

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("👤 Total Users", len(users))
col2.metric("📊 Predictions", len(history))
col3.metric("⚡ Active Admin", "YES")

# =========================
# USERS TABLE
# =========================
st.subheader("👥 Users Management")
st.dataframe(users)

# =========================
# DELETE USER
# =========================
st.markdown("### ❌ Delete User")

user_to_delete = st.text_input("Username to delete")

if st.button("Delete User"):

    if user_to_delete:

        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username=?", (user_to_delete,))
        conn.commit()

        st.success(f"User {user_to_delete} deleted ✅")

# =========================
# HISTORY CONTROL
# =========================
st.subheader("📊 All Predictions")

st.dataframe(history)

# =========================
# CLEAR HISTORY
# =========================
if st.button("🧹 Clear All History"):

    c = conn.cursor()
    c.execute("DELETE FROM history")
    conn.commit()

    st.warning("All history cleared ⚠️")