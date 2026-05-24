import streamlit as st
from db import init_db, add_user, check_user

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Login", page_icon="🔐")

# =========================
# INIT DB (once)
# =========================
init_db()

# =========================
# SESSION STATE SAFETY
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# =========================
# TITLE
# =========================
st.title("🔐 MindCare AI Login System")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

# =========================
# LOGIN
# =========================
with tab1:

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):

        if username and password:

            user = check_user(username, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.user = username

                st.success("Login successful ✅")

                st.switch_page("pages/Dashboard.py")

            else:
                st.error("Invalid credentials ❌")

        else:
            st.warning("Please fill all fields")

# =========================
# SIGN UP
# =========================
with tab2:

    new_user = st.text_input("New Username", key="new_user")
    new_pass = st.text_input("New Password", type="password", key="new_pass")

    if st.button("Create Account", key="signup_btn"):

        if new_user and new_pass:

            success = add_user(new_user, new_pass)

            if success:
                st.success("Account created 🎉 Please login now")
            else:
                st.error("Username already exists ❌")

        else:
            st.warning("Fill all fields")
