import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Student Risk Dashboard", layout="wide")

# ---------------- BACKGROUND IMAGE ----------------
def set_bg():
    try:
        with open("bg.jpg", "rb") as file:
            encoded = base64.b64encode(file.read()).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            /* Dark overlay for readability */
            .stApp::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.4);
                z-index: -1;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    except FileNotFoundError:
        st.error("❌ bg.jpg not found. Please place it in the same folder as this file.")

set_bg()

# ---------------- GLASS UI CSS ----------------
st.markdown("""
<style>

.card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 15px;
    padding: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    color: white;
}

[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(10px);
}

.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
}

h1, h2, h3, h4, p {
    color: white;
}

.card:hover {
    transform: scale(1.05);
    transition: 0.3s;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
model = joblib.load("model.pkl")
data = pd.read_csv("data.csv")

# ---------------- LOGIN ----------------
st.sidebar.title("🔐 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username != "Afrin" or password != "666":
    st.warning("Please login to continue")
    st.stop()

st.sidebar.success("Login Successful")

# ---------------- NAVIGATION ----------------
page = st.sidebar.selectbox("Navigate", [
    "🏠 Dashboard",
    "📊 Analytics",
    "🔍 Student Analysis",
    "⚠️ Risk Alerts",
    "🤖 Prediction",
    "📥 Reports"
])

# =========================================================
# 🏠 DASHBOARD
# =========================================================
if page == "🏠 Dashboard":

    st.markdown("<h1 style='text-align:center;'>🎓 AI Student Risk Dashboard</h1>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"<div class='card'><h4>Total Students</h4><h2>{len(data)}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'><h4>High Risk</h4><h2>{len(data[data['risk']=='High'])}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'><h4>Medium Risk</h4><h2>{len(data[data['risk']=='Medium'])}</h2></div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='card'><h4>Low Risk</h4><h2>{len(data[data['risk']=='Low'])}</h2></div>", unsafe_allow_html=True)

    st.markdown("---")

    col5, col6 = st.columns(2)

    with col5:
        fig1 = px.pie(data, names="risk", title="Risk Distribution")
        st.plotly_chart(fig1, use_container_width=True)

    with col6:
        fig2 = px.bar(data, x="risk", title="Risk Count")
        st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# 📊 ANALYTICS
# =========================================================
elif page == "📊 Analytics":

    st.title("📊 Analytics")

    fig = px.scatter(data, x="attendance", y="marks", color="risk")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.line(data, y=["attendance", "marks"])
    st.plotly_chart(fig2, use_container_width=True)

    from sklearn.metrics import confusion_matrix, accuracy_score
    import matplotlib.pyplot as plt
    import seaborn as sns

    X = data[["attendance","marks","assignments","prev_gpa"]]
    y = data["risk"]

    pred = model.predict(X)
    acc = accuracy_score(y, pred)

    st.subheader(f"Model Accuracy: {acc:.2f}")

    cm = confusion_matrix(y, pred)

    fig3, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    st.pyplot(fig3)

# =========================================================
# 🔍 STUDENT ANALYSIS
# =========================================================
elif page == "🔍 Student Analysis":

    st.title("🔍 Student Analysis")

    index = st.selectbox("Select Student", data.index)
    student = data.loc[index]

    st.write(student)

    fig = px.bar(
        x=["Attendance","Marks","Assignments","GPA"],
        y=[student["attendance"], student["marks"], student["assignments"], student["prev_gpa"]],
        title="Performance"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# ⚠️ RISK ALERTS
# =========================================================
elif page == "⚠️ Risk Alerts":

    st.title("⚠️ High Risk Students")

    high_risk = data[data["risk"] == "High"]

    if len(high_risk) > 0:
        st.error("Immediate Attention Required")
        st.dataframe(high_risk)
    else:
        st.success("No High Risk Students")

# =========================================================
# 🤖 PREDICTION
# =========================================================
elif page == "🤖 Prediction":

    st.title("🤖 Predict Student Risk")

    attendance = st.slider("Attendance %", 0, 100, 70)
    marks = st.slider("Marks", 0, 100, 60)
    assignments = st.slider("Assignments", 0, 100, 65)
    prev_gpa = st.slider("Previous GPA", 0.0, 10.0, 6.5)

    if st.button("Predict"):
        result = model.predict([[attendance, marks, assignments, prev_gpa]])[0]
        prob = model.predict_proba([[attendance, marks, assignments, prev_gpa]])

        st.subheader(f"Prediction: {result}")
        st.write(f"Confidence: {max(prob[0]):.2f}")

        if result == "High":
            st.error("⚠️ High Risk Student")
        elif result == "Medium":
            st.warning("⚠️ Medium Risk Student")
        else:
            st.success("✅ Low Risk Student")

        if attendance < 60:
            rec = "Improve attendance"
        elif marks < 50:
            rec = "Focus on academics"
        else:
            rec = "Good performance"

        st.info(f"📌 Recommendation: {rec}")

# =========================================================
# 📥 REPORTS
# =========================================================
elif page == "📥 Reports":

    st.title("📥 Reports")

    st.dataframe(data)

    st.download_button(
        "Download CSV",
        data.to_csv(index=False),
        "student_report.csv"
    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("🎓 Developed for AI Student Risk Prediction Project")