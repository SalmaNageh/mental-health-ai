import streamlit as st
from db import init_db, add_user, check_user,create_admin

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Login", page_icon="🔐")

# =========================
# INIT DB
# =========================
init_db()
create_admin()
# =========================
# SESSION STATE SAFE INIT
# =========================
defaults = {
    "logged_in": False,
    "user": None,
    "role": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
                # user = (username, role)

                st.session_state.logged_in = True
                st.session_state.user = user[0]
                st.session_state.role = user[1]

                st.success(f"Welcome {user[0]} 👋")

                # Redirect based on role
                if user[1] == "admin":
                    st.switch_page("pages/Admin.py")
                else:
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
