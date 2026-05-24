import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="MindCare AI",
    page_icon="🧠"
)

with st.sidebar:

    page = option_menu(
        "🧠 MindCare AI",
        ["Login", "Dashboard", "Analytics", "Model Performance"],
        icons=["lock", "cpu", "bar-chart"],
        default_index=0
    )
st.write("Use sidebar navigation")
if page == "Login":

    st.switch_page("pages/Login.py")

elif page == "Dashboard":

    st.switch_page("pages/Dashboard.py")

elif page == "Analytics":

    st.switch_page("pages/Analytics.py")
elif page == "Model Performance":
    st.switch_page("pages/Model_Performance.py")