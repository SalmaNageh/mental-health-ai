import streamlit as st
from db import init_db, add_user, check_user

st.set_page_config(page_title="Login")

# init database
init_db()

st.title("🔐 Login System (SQLite)")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

# =========================
# LOGIN
# =========================
with tab1:

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = check_user(username, password)

        if user:

            st.session_state.logged_in = True
            st.session_state.user = username

            st.success("Login successful ✅")
            st.switch_page("pages/Dashboard.py")

        else:
            st.error("Invalid credentials ❌")


# =========================
# SIGN UP
# =========================
with tab2:

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password")

    if st.button("Create Account"):

        if new_user == "" or new_pass == "":
            st.warning("Fill all fields")
        else:
            success = add_user(new_user, new_pass)

            if success:
                st.success("Account created 🎉")
            else:
                st.error("Username already exists ❌")
