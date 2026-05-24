import streamlit as st
import joblib
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, f1_score

from auth import check_login

check_login()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Model Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOAD DATA + MODEL
# =========================
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

df = pd.read_csv("Combined Data.csv").dropna()

# =========================
# CLEAN TEXT
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_text"] = df["statement"].apply(clean_text)

X = df["clean_text"]
y = df["status"]

X_vec = vectorizer.transform(X)
y_pred = model.predict(X_vec)

labels = sorted(y.unique())

# =========================
# METRICS
# =========================
acc = accuracy_score(y, y_pred)
f1 = f1_score(y, y_pred, average="weighted")

# =========================
# STYLING (CARDS + ANIMATION)
# =========================
st.markdown("""
<style>

/* background */
.stApp {
    background: linear-gradient(120deg, #0f172a, #111827);
    color: white;
}

/* card */
.card {
    padding: 20px;
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    transition: 0.3s;
    text-align: center;
    animation: fadeIn 0.8s ease-in-out;
}

.card:hover {
    transform: scale(1.05);
    background: rgba(255,255,255,0.08);
}

/* animation */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* title */
.title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown("<div class='title'>📊 AI Model Performance Dashboard</div>", unsafe_allow_html=True)

# =========================
# KPI CARDS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
        <h3>🎯 Accuracy</h3>
        <h2>{acc*100:.2f}%</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <h3>📊 F1 Score</h3>
        <h2>{f1*100:.2f}%</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <h3>🧠 Samples</h3>
        <h2>{len(df)}</h2>
    </div>
    """, unsafe_allow_html=True)

# =========================
# CONFUSION MATRIX
# =========================
st.markdown("## 🔥 Confusion Matrix")

cm = confusion_matrix(y, y_pred, labels=labels)

fig, ax = plt.subplots(figsize=(10,6))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="coolwarm",
    xticklabels=labels,
    yticklabels=labels
)

plt.xlabel("Predicted")
plt.ylabel("Actual")

st.pyplot(fig)

# =========================
# CLASSIFICATION REPORT
# =========================
st.markdown("## 📄 Classification Report")

report = classification_report(y, y_pred, output_dict=True)

st.dataframe(pd.DataFrame(report).transpose())

# =========================
# FOOTER
# =========================
st.markdown("""
<div style="text-align:center; margin-top:40px; color:gray;">
🚀 Built with Streamlit | AI Mental Health System
</div>
""", unsafe_allow_html=True)
