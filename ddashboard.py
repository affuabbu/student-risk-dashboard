import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Student Risk System", layout="wide")

# ---------------- UI + ANIMATION CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(rgba(10,10,20,0.85), rgba(10,10,20,0.95)),
                url("bg.jpg");
    background-size: cover;
    background-attachment: fixed;
    font-family: 'Segoe UI', sans-serif;
}

/* Glass Card with animation */
.glass {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    color: white;
    text-align: center;

    opacity: 0;
    transform: translateY(30px);
    animation: fadeInUp 0.8s ease forwards;
}

/* Animation */
@keyframes fadeInUp {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Stagger effect */
.glass:nth-child(1) { animation-delay: 0.1s; }
.glass:nth-child(2) { animation-delay: 0.2s; }
.glass:nth-child(3) { animation-delay: 0.3s; }
.glass:nth-child(4) { animation-delay: 0.4s; }

.glass:hover {
    transform: scale(1.03);
    transition: 0.3s;
}

/* Title */
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: white;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #cccccc;
}

/* Button */
.stButton button {
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    color: white;
    border-radius: 10px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.6);
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
users = {"admin":"1234", "faculty":"pass"}

if "login" not in st.session_state:
    st.session_state["login"] = False

if not st.session_state["login"]:
    st.markdown("<h2 style='text-align:center;color:white;'>🔐 Login</h2>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in users and users[u] == p:
            st.session_state["login"] = True
        else:
            st.error("Invalid Credentials")
    st.stop()

# ---------------- LOADING ANIMATION ----------------
with st.spinner("🚀 Loading AI Dashboard..."):
    time.sleep(1)

# ---------------- TITLE ----------------
st.markdown("<div class='title'>🎓 EduPredict AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Analytics • Early Risk Detection • Faculty Insights</div>", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data.csv")

subjects = ["Data Structures","Operating Systems","DBMS","Computer Networks","Java Programming"]

# ---------------- CALCULATIONS ----------------
df["Average"] = df[subjects].mean(axis=1)

def risk(row):
    if row["Average"] < 50 or row["Attendance"] < 60 or row["Sleep Hours"] < 5:
        return "High Risk"
    elif row["Average"] < 70 or row["Sleep Hours"] < 6:
        return "Medium Risk"
    else:
        return "Low Risk"

df["Risk Level"] = df.apply(risk, axis=1)

df["Confidence"] = [round(random.uniform(80,95),2) for _ in range(len(df))]

def suggestion(level):
    if level == "High Risk":
        return "⚠ Counseling, extra classes, improve sleep, strict attendance"
    elif level == "Medium Risk":
        return "📘 Mentoring, practice, maintain sleep"
    else:
        return "✅ Encourage projects, internships"

df["Faculty Action"] = df["Risk Level"].apply(suggestion)

# ---------------- SEARCH ----------------
search = st.text_input("🔍 Search Student (Name / ID)")

if search:
    df = df[df["Name"].str.contains(search, case=False) | df["Student_ID"].astype(str).str.contains(search)]

# ---------------- FILTERS ----------------
st.sidebar.header("Filters")

risk_filter = st.sidebar.multiselect("Risk Level", df["Risk Level"].unique(), default=df["Risk Level"].unique())

low_att = st.sidebar.checkbox("Low Attendance (<60%)")
low_sleep = st.sidebar.checkbox("Low Sleep (<6 hrs)")

df = df[df["Risk Level"].isin(risk_filter)]

if low_att:
    df = df[df["Attendance"] < 60]

if low_sleep:
    df = df[df["Sleep Hours"] < 6]

# ---------------- KPI ----------------
c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='glass'><h3>Total Students</h3><h1>{len(df)}</h1></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='glass'><h3>High Risk</h3><h1>{len(df[df['Risk Level']=='High Risk'])}</h1></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='glass'><h3>Medium Risk</h3><h1>{len(df[df['Risk Level']=='Medium Risk'])}</h1></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='glass'><h3>Low Risk</h3><h1>{len(df[df['Risk Level']=='Low Risk'])}</h1></div>", unsafe_allow_html=True)

# ---------------- AI INSIGHTS ----------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("### 🧠 AI Insights")

high = df[df["Risk Level"]=="High Risk"]

if not high.empty:
    st.error(f"{len(high)} students need immediate attention")
else:
    st.success("All students performing well")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ADVANCED ANALYTICS ----------------
st.markdown("### 📊 Advanced Analytics")

avg_marks = round(df["Average"].mean(),2)
avg_att = round(df["Attendance"].mean(),2)
avg_sleep = round(df["Sleep Hours"].mean(),2)

st.info(f"""
📊 Avg Marks: {avg_marks}  
📉 Avg Attendance: {avg_att}%  
😴 Avg Sleep: {avg_sleep} hrs
""")

# ---------------- TABLE ----------------
st.dataframe(df, use_container_width=True)

# ---------------- CHARTS ----------------
st.plotly_chart(px.pie(df, names="Risk Level", title="Risk Distribution"), use_container_width=True)
st.plotly_chart(px.bar(df, x="Name", y="Average", color="Risk Level"), use_container_width=True)
st.plotly_chart(px.scatter(df, x="Attendance", y="Average", color="Risk Level", size="Average"), use_container_width=True)

# ---------------- RADAR ----------------
st.markdown("### 📊 Student Radar")
name = st.selectbox("Select Student", df["Name"])
student = df[df["Name"]==name].iloc[0]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=[student[s] for s in subjects],
    theta=subjects,
    fill='toself'
))
st.plotly_chart(fig)

# ---------------- STUDENT CARD ----------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)

st.markdown(f"""
### 🎯 Student Analysis

👤 {student['Name']}  
📊 Avg: {round(student['Average'],2)}  
📉 Attendance: {student['Attendance']}%  
😴 Sleep: {student['Sleep Hours']} hrs  
⚠ Risk: {student['Risk Level']}  
🎯 Confidence: {student['Confidence']}%

🧠 Suggestion:  
{student['Faculty Action']}
""")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- AI CHATBOT ----------------
st.markdown("<div class='glass'>", unsafe_allow_html=True)

st.markdown("### 🤖 AI Assistant")

user_input = st.text_input("Ask something like: high risk / attendance / sleep / top student")

if user_input:
    q = user_input.lower()

    high_count = len(df[df['Risk Level'] == 'High Risk'])
    avg_att = round(df['Attendance'].mean(),2)
    avg_sleep = round(df['Sleep Hours'].mean(),2)

    if "high risk" in q:
        st.error(f"⚠ {high_count} students are at HIGH RISK. Immediate attention needed.")

    elif "attendance" in q:
        st.info(f"📉 Average attendance is {avg_att}%.")

        if avg_att < 65:
            st.warning("⚠ Attendance is low. Suggest strict monitoring.")

    elif "sleep" in q:
        st.info(f"😴 Average sleep is {avg_sleep} hours.")

        if avg_sleep < 6:
            st.warning("⚠ Students are not getting enough sleep.")

    elif "top student" in q:
        top = df.sort_values("Average", ascending=False).iloc[0]
        st.success(f"🏆 Top student: {top['Name']} with {round(top['Average'],2)} marks.")

    elif "suggest" in q or "recommend" in q:
        st.write("📌 General Suggestion: Focus on attendance, sleep, and regular study.")

    else:
        st.warning("🤖 Try: high risk / attendance / sleep / top student / suggest")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- DOWNLOAD ----------------
st.download_button("📄 Download Report", df.to_csv(index=False), "report.csv")