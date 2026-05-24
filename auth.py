import streamlit as st

def init_users():
    if "users" not in st.session_state:
        st.session_state.users = {
            "admin": "1234",
            "sola": "5678"
        }

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user" not in st.session_state:
        st.session_state.user = None


def check_login():
    init_users()

    if not st.session_state.logged_in:
        st.warning("🔒 Please login first")
        st.stop()


if st.sidebar.button("Logout", key="logout_btn"):

    st.session_state.logged_in = False
    st.session_state.user = None

    st.switch_page("pages/Login.py")