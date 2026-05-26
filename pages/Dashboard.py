import streamlit as st
import joblib
import re
import numpy as np
import time
import requests
from streamlit_lottie import st_lottie

from db import init_db, add_history
from auth import check_login

# =========================
# INIT DB
# =========================
init_db()

# =========================
# AUTH
# =========================
check_login()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="MindCare AI",
    page_icon="🧠",
    layout="wide"
)

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_models():

    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")

    return model, vectorizer


model, vectorizer = load_models()

# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "user" not in st.session_state:
    st.session_state.user = "User"

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
st.markdown("""
<div style="
    font-size:45px;
    text-align:center;
    font-weight:bold;
    background: linear-gradient(90deg,#60a5fa,#a78bfa);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
">
🧠 MindCare AI
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    text-align:center;
    color:gray;
    margin-bottom:30px;
">
AI Mental Health Analysis Dashboard
</div>
""", unsafe_allow_html=True)

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric(
    "🧠 Total Predictions",
    len(st.session_state.history)
)

col2.metric(
    "📊 System",
    "AI Active"
)

col3.metric(
    "⚡ Status",
    "Running"
)

# =========================
# INPUT
# =========================
text = st.text_area(
    "💬 Write how you feel:",
    height=170
)

# =========================
# CLEAN TEXT
# =========================
def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"[^a-zA-Z\s]", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

# =========================
# LOAD LOTTIE
# =========================
def load_lottie(url):

    try:

        r = requests.get(url)

        if r.status_code != 200:
            return None

        return r.json()

    except:
        return None

# =========================
# ANALYZE BUTTON
# =========================
if st.button("Analyze"):

    if text.strip() == "":

        st.warning("Please enter text")

    else:

        with st.spinner("🧠 AI analyzing mental state..."):

            time.sleep(2)

        # =========================
        # CLEAN + PREDICT
        # =========================
        cleaned = clean_text(text)

        vector = vectorizer.transform([cleaned])

        prediction = model.predict(vector)[0]

        score = np.max(model.decision_function(vector))

        confidence = min(abs(score) / 3, 1)

        # =========================
        # SAVE TO DB
        # =========================
        add_history(
            st.session_state.user,
            cleaned,
            prediction,
            float(confidence)
        )

        # =========================
        # SAVE SESSION
        # =========================
        st.session_state.history.append(prediction)

        # =========================
        # LOTTIE ANIMATION
        # =========================
        url = "https://assets9.lottiefiles.com/packages/lf20_t9gkkhz4.json"

        animation = load_lottie(url)

        if animation:

            st_lottie(
                animation,
                height=200
            )

        # =========================
        # RESULT COLORS
        # =========================
        if prediction == "Normal":

            color = "#22c55e"

        elif prediction in ["Depression", "Suicidal"]:

            color = "#ef4444"

        else:

            color = "#f59e0b"

        # =========================
        # RESULT CARD
        # =========================
        st.markdown(f"""
        <div style="
            padding:25px;
            border-radius:20px;
            background:linear-gradient(135deg,{color},#0f172a);
            color:white;
            text-align:center;
            font-size:25px;
            font-weight:bold;
            margin-top:20px;
            box-shadow:0 8px 30px rgba(0,0,0,0.3);
        ">
        Prediction: {prediction}
        <br><br>
        Confidence: {confidence*100:.1f}%
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # PROGRESS BAR
        # =========================
        st.markdown("### 📊 Confidence Meter")

        st.progress(confidence)

        # =========================
        # SUPPORT MESSAGE
        # =========================
        messages = {

            "Anxiety":
            "Try to slow down and focus on breathing.",

            "Depression":
            "Talk to someone you trust 💙",

            "Stress":
            "Take breaks and rest properly.",

            "Normal":
            "You seem emotionally balanced ✨",

            "Suicidal":
            "Please seek professional support immediately.",

            "Bipolar":
            "Maintain routine and stability.",

            "Personality disorder":
            "Self-awareness and support can help a lot."
        }

        st.info(
            messages.get(
                prediction,
                "Take care of yourself 💙"
            )
        )

# =========================
# HISTORY
# =========================
st.markdown("## 🕘 Recent Predictions")

if st.session_state.history:

    for item in st.session_state.history[-5:][::-1]:

        st.markdown(f"""
        <div style="
            background:#1e293b;
            padding:15px;
            margin:10px 0;
            border-radius:15px;
            color:white;
            border:1px solid #334155;
        ">
        {item}
        </div>
        """, unsafe_allow_html=True)

else:

    st.write("No predictions yet")
