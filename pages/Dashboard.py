import streamlit as st
import joblib
import re
import numpy as np
import time
from streamlit_lottie import st_lottie
import requests

from auth import check_login

# =========================
# AUTH
# =========================
check_login()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard",
    page_icon="🧠",
    layout="centered"
)

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

if "user" not in st.session_state:
    st.session_state.user = "User"

# =========================
# SIDEBAR
# =========================
st.sidebar.success(f"👋 Welcome {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.switch_page("pages/Login.py")

# =========================
# LOTTIE
# =========================
def load_lottie(url):
    r = requests.get(url)
    return r.json()

lottie_ai = load_lottie(
    "https://assets9.lottiefiles.com/packages/lf20_t9gkkhz4.json"
)

st_lottie(lottie_ai, height=200)

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: white;
}

.stTextArea textarea {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 12px;
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("🧠 Mental Health Dashboard")
st.markdown("Analyze emotions using NLP & Machine Learning")

# =========================
# INPUT
# =========================
text = st.text_area("Write how you feel:", height=180)

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
# ANALYZE
# =========================
if st.button("Analyze"):

    if text.strip() == "":
        st.warning("Please enter text")

    else:

        with st.spinner("Analyzing mental state..."):
            time.sleep(2)

        cleaned = clean_text(text)

        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]

        # =========================
        # SAVE STATE
        # =========================
        st.session_state.history.append(prediction)
        st.session_state.last_vector = vector
        st.session_state.last_text = cleaned

        # =========================
        # CONFIDENCE
        # =========================
        score = np.max(model.decision_function(vector))
        confidence = min(abs(score) / 3, 1)

        # COLORS
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
            background: linear-gradient(135deg, {color}, #0f172a);
            color:white;
            font-size:24px;
            text-align:center;
            font-weight:bold;
            margin-top:20px;
        ">
        Prediction: {prediction}
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # CONFIDENCE
        # =========================
        st.markdown("### Confidence Meter")
        st.progress(confidence)
        st.write(f"{confidence*100:.1f}% confidence")

        # =========================
        # SUPPORT MESSAGE
        # =========================
        messages = {
            "Anxiety": "Try to slow down and focus on one task at a time.",
            "Depression": "Talk to someone you trust.",
            "Stress": "Take breaks and rest.",
            "Normal": "You seem emotionally balanced ✨",
            "Suicidal": "Please seek professional support.",
            "Bipolar": "Maintain routine and stability.",
            "Personality disorder": "Self-awareness helps a lot."
        }

        st.info(messages.get(prediction, "Take care of yourself 💙"))

# =========================
# EXPLAINABLE AI (FIXED)
# =========================
if "last_vector" in st.session_state:

    st.markdown("### 🧠 Why this prediction?")

    vector = st.session_state.last_vector

    feature_names = vectorizer.get_feature_names_out()

    vector_array = vector.toarray()[0]

    top_indices = vector_array.argsort()[::-1][:5]

    top_words = [
        feature_names[i]
        for i in top_indices
        if vector_array[i] > 0
    ]

    if top_words:
        st.success("Key words: " + ", ".join(top_words))
    else:
        st.info("No strong keywords detected")
