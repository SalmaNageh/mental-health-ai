import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="MindCare AI",
    page_icon="🧠"
)

with st.sidebar:

    option_menu(
        "🧠 MindCare AI",
        ["Login", "Dashboard", "Analytics", "Model Performance"],
        icons=["lock", "cpu", "bar-chart", "graph-up"],
        default_index=0
    )

st.title("🧠 MindCare AI")

st.write("Use the sidebar to navigate between pages.")