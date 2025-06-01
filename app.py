import streamlit as st
import openai
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Study Buddy", page_icon="🎓")

# Session state to persist info
if "history" not in st.session_state:
    st.session_state.history = []
if "reminders" not in st.session_state:
    st.session_state.reminders = {}

# Sidebar
st.sidebar.title("📚 Study Buddy Menu")
selected_agent = st.sidebar.radio("Choose your assistant", ["Concept Explainer", "Quiz Master", "Study Planner"])
topic = st.sidebar.text_input("Enter your topic", "Linear Regression")

st.title("🎓 AI Study Buddy")

# ----------------------------- AGENT FUNCTIONS -----------------------------

def ask_openai(prompt, temperature=0.7):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Using GPT-4 Mini model
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()


def concept_explainer(topic):
    prompt = f"Explain the concept of {topic} in simple terms with a short example."
    return ask_openai(prompt)


def quiz_master(topic):
    prompt = f"Create a short 3-question quiz with answers on the topic: {topic}."
    return ask_openai(prompt)


def study_planner(topic, date):
    msg = f"You have scheduled a revision of '{topic}' on {date.strftime('%Y-%m-%d')}."
    st.session_state.reminders[topic] = date
    return msg

# ----------------------------- AGENT INTERFACE -----------------------------

if selected_agent == "Concept Explainer":
    st.subheader("📘 Concept Explainer")
    if st.button("Explain"):
        explanation = concept_explainer(topic)
        st.info(explanation)
        st.session_state.history.append(("Explained", topic))

elif selected_agent == "Quiz Master":
    st.subheader("🧠 Quiz Master")
    if st.button("Generate Quiz"):
        quiz = quiz_master(topic)
        st.success(quiz)
        st.session_state.history.append(("Quiz", topic))

elif selected_agent == "Study Planner":
    st.subheader("⏰ Study Planner")
    date = st.date_input("Pick a revision date", datetime.date.today())
    if st.button("Set Reminder"):
        msg = study_planner(topic, date)
        st.success(msg)
        st.session_state.history.append(("Reminder Set", topic))

# ----------------------------- HISTORY -----------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("🕓 History")
for action, item in st.session_state.history:
    st.sidebar.write(f"{action}: {item}")

# ----------------------------- REMINDERS -----------------------------
if st.session_state.reminders:
    st.sidebar.markdown("---")
    st.sidebar.subheader("⏰ Upcoming Reminders")
    today = datetime.date.today()
    for t, d in st.session_state.reminders.items():
        days_left = (d - today).days
        st.sidebar.write(f"{t}: in {days_left} day(s)")
