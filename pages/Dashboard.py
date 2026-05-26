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
# INIT DB (safe)
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
# LOAD MODEL (CACHE FIX)
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
st.sidebar.success(f"👋 Welcome {st.session_state.user}")

# =========================
# TITLE
# =========================
st.markdown("<div style='font-size:40px;text-align:center;font-weight:bold'>🧠 MindCare AI</div>", unsafe_allow_html=True)

st.markdown("<div style='text-align:center;color:gray'>AI Mental Health Analysis Dashboard</div>", unsafe_allow_html=True)

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("🧠 Total Predictions", len(st.session_state.history))
col2.metric("📊 System", "AI Active")
col3.metric("⚡ Status", "Running")

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
# LOTTIE
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
# ANALYZE
# =========================
if st.button("Analyze"):

    if text.strip() == "":
        st.warning("Please enter text")

    else:
        with st.spinner("🧠 AI analyzing..."):
            time.sleep(2)

        cleaned = clean_text(text)

        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]

        score = np.max(model.decision_function(vector))
        confidence = min(abs(score) / 3, 1)

        # ================= SAVE TO DB =================
        add_history(
            st.session_state.user,
            cleaned,
            prediction,
            float(confidence)
        )

        st.session_state.history.append(prediction)

        # ================= LOTTIE =================
        if prediction == "Depression":
            

if prediction == "Depression":

    url = "https://assets9.lottiefiles.com/packages/lf20_t9gkkhz4.json"

elif prediction == "Anxiety":

    url = "https://assets9.lottiefiles.com/packages/lf20_t9gkkhz4.json"

else:

    url = "https://assets9.lottiefiles.com/packages/lf20_t9gkkhz4.json"


animation = load_lottie(url)

if animation:

    st_lottie(animation, height=180)
        # ================= RESULT =================
        st.markdown(f"""
        <div style="
            padding:20px;
            border-radius:20px;
            background:linear-gradient(135deg,#2563eb,#0f172a);
            color:white;
            text-align:center;
            font-size:22px;
        ">
        Prediction: {prediction} <br>
        Confidence: {confidence*100:.1f}%
        </div>
        """, unsafe_allow_html=True)

        st.progress(confidence)

        messages = {
            "Anxiety": "Try to breathe slowly.",
            "Depression": "Talk to someone you trust.",
            "Stress": "Take breaks.",
            "Normal": "You are doing great ✨",
            "Suicidal": "Please seek help immediately."
        }

        st.info(messages.get(prediction, "Take care 💙"))

# =========================
# HISTORY
# =========================
st.markdown("### 🕘 Recent Predictions")

if st.session_state.history:
    for h in st.session_state.history[-5:][::-1]:
        st.markdown(f"""
        <div style="
            padding:10px;
            margin:5px;
            border-radius:10px;
            background:#1e293b;
            color:white;
        ">
        {h}
        </div>
        """, unsafe_allow_html=True)
else:
    st.write("No predictions yet")
