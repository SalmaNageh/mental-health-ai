import streamlit as st
import joblib
import re
import numpy as np
import time
import requests
from streamlit_lottie import st_lottie
from db import init_db, add_history
init_db()

from auth import check_login

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
# THEME TOGGLE
# =========================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if st.sidebar.button("🌓 Toggle Theme"):
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# =========================
# COLORS
# =========================
if st.session_state.theme == "dark":
    bg = "#0b1220"
    card = "#1e293b"
    text = "white"
else:
    bg = "#f1f5f9"
    card = "white"
    text = "black"

# =========================
# CSS (GLASS + UI)
# =========================
st.markdown(f"""
<style>

.stApp {{
    background-color: {bg};
    color: {text};
}}

.title {{
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.subtitle {{
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}}

.card {{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: 0.3s;
}}

.card:hover {{
    transform: scale(1.03);
}}

.stButton>button {{
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-weight: bold;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
}}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# SIDEBAR
# =========================
st.sidebar.success("👋 Welcome back!")

# =========================
# TITLE
# =========================
st.markdown("<div class='title'>🧠 MindCare AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI Mental Health Analysis Dashboard</div>", unsafe_allow_html=True)

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("🧠 Total Predictions", len(st.session_state.history))
col2.metric("📊 System", "AI Active")
col3.metric("⚡ Status", "Running")

# =========================
# LOTTIE
# =========================
def load_lottie(url):
    return requests.get(url).json()

# =========================
# INPUT
# =========================
text = st.text_area("💬 Write how you feel:", height=150)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# =========================
# ANALYZE
# =========================
if st.button("Analyze"):

    if text.strip() == "":
        st.warning("Please enter text")

    else:
        with st.spinner("🧠 AI is analyzing..."):
            time.sleep(2)

        cleaned = clean_text(text)

        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]

        st.session_state.history.append(prediction)

        score = np.max(model.decision_function(vector))
        confidence = min(abs(score) / 3, 1)

        # ================= LOTTIE =================
        if prediction == "Depression":
            url = "https://assets2.lottiefiles.com/packages/lf20_depression.json"
        elif prediction == "Anxiety":
            url = "https://assets2.lottiefiles.com/packages/lf20_anxiety.json"
        else:
            url = "https://assets9.lottiefiles.com/packages/lf20_t9gkkhz4.json"

        st_lottie(load_lottie(url), height=180)

        # ================= RESULT CARD =================
        st.markdown(f"""
        <div class="card" style="margin-top:20px;">
            <h2>Prediction: {prediction}</h2>
            <p>Confidence: {confidence*100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(confidence)

        # ================= SUPPORT =================
        messages = {
            "Anxiety": "Try to slow down and breathe.",
            "Depression": "Talk to someone you trust.",
            "Stress": "Take breaks and rest.",
            "Normal": "You are doing great ✨",
            "Suicidal": "Please seek help immediately."
        }

        st.info(messages.get(prediction, "Take care 💙"))
        
add_history(
    st.session_state.user,
    cleaned,
    prediction,
    float(confidence)
)
# =========================
# HISTORY
# =========================
st.markdown("### 🕘 Recent Predictions")

if st.session_state.history:
    for h in st.session_state.history[-5:][::-1]:
        st.markdown(f"""
        <div class="card">
            {h}
        </div>
        """, unsafe_allow_html=True)
else:
    st.write("No predictions yet")
