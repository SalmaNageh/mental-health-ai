import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

from auth import check_login

# =========================
# AUTH
# =========================
check_login()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="centered"
)

# =========================
# SESSION
# =========================
if "history" not in st.session_state:

    st.session_state.history = []

# =========================
# SIDEBAR
# =========================
st.sidebar.success(
    f"👋 Welcome {st.session_state.user}"
)

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.user = None

    st.switch_page("pages/Login.py")

# =========================
# TITLE
# =========================
st.title("📊 Analytics Dashboard")

# DEBUG
st.write("History:", st.session_state.history)

# =========================
# PIE CHART
# =========================
st.markdown("## 🥧 Prediction Statistics")

if len(st.session_state.history) > 0:

    data = Counter(st.session_state.history)

    fig, ax = plt.subplots(figsize=(5,5))

    ax.pie(
        data.values(),
        labels=data.keys(),
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)

else:

    st.info("No prediction history yet")

# =========================
# WORD CLOUD
# =========================
st.markdown("## ☁️ Word Cloud")

if len(st.session_state.history) > 0:

    all_text = " ".join(
        st.session_state.history
    )

    wc = WordCloud(
        width=800,
        height=400,
        background_color="black"
    ).generate(all_text)

    fig, ax = plt.subplots(figsize=(10,5))

    ax.imshow(wc)

    ax.axis("off")

    st.pyplot(fig)

else:

    st.info("No data available")

# =========================
# HISTORY
# =========================
st.markdown("## 🕘 Recent Predictions")

if len(st.session_state.history) > 0:

    for item in st.session_state.history[::-1]:

        st.markdown(f"""
        <div style="
            background-color:#111827;
            padding:12px;
            margin:8px 0;
            border-radius:12px;
            border:1px solid #1f2937;
            color:white;
        ">
        {item}
        </div>
        """, unsafe_allow_html=True)

else:

    st.write("No predictions yet")