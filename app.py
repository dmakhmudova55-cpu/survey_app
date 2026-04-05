import streamlit as st
import json
from datetime import datetime

# ---------------- DATA ----------------
version_float = 2.0

questions = [
    {"q": "How familiar are you with the Pomodoro Technique?",
     "opts": [("Never heard of it",0),("Heard of it but never tried",1),("Tried it occasionally",2),("Use it regularly",3)]},

    {"q": "How often do you use timed study intervals?",
     "opts": [("Never",0),("Occasionally",1),("Several times per week",2),("Daily",3)]},

    {"q": "Can you focus for a full Pomodoro session (25 minutes)?",
     "opts": [("Never",0),("Sometimes",1),("Most of the time",2),("Always",3)]},

    {"q": "Do you track your Pomodoros?",
     "opts": [("Never",0),("Rarely",1),("Often",2),("Always",3)]},

    {"q": "How many Pomodoros do you complete in a typical study session?",
     "opts": [("1 or none",0),("2-3",1),("4-5",2),("6 or more",3)]},

    {"q": "Using Pomodoro improves your focus.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Agree",2),("Strongly agree",3)]},

    {"q": "Does Pomodoro make starting tasks easier?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Significantly",3)]},

    {"q": "Does Pomodoro help you prioritize tasks effectively?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Very much",3)]},

    {"q": "Pomodoro helps you manage tasks efficiently.",
     "opts": [("Strongly disagree",0),("Disagree",1),("Agree",2),("Strongly agree",3)]},

    {"q": "How effective is Pomodoro for reducing distractions?",
     "opts": [("Not effective",0),("Somewhat effective",1),("Effective",2),("Very effective",3)]},

    {"q": "Does using Pomodoro increase your productivity?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Significantly",3)]},

    {"q": "Does Pomodoro increase your engagement during study sessions?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Very much",3)]},

    {"q": "Does Pomodoro help you complete tasks on time?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Always helps",3)]},

    {"q": "Do breaks between Pomodoros improve your motivation?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Very much",3)]},

    {"q": "Do you feel a sense of accomplishment after each Pomodoro?",
     "opts": [("Never",0),("Sometimes",1),("Often",2),("Always",3)]},

    {"q": "Does Pomodoro help you stay consistent in your study schedule?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Very much",3)]},

    {"q": "Does Pomodoro help you complete complex tasks efficiently?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Very much",3)]},

    {"q": "Are you satisfied with your productivity using Pomodoro?",
     "opts": [("Never",0),("Sometimes",1),("Often",2),("Always",3)]},

    {"q": "In general, does Pomodoro improve your study performance?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Significantly",3)]},

    {"q": "How likely are you to continue using Pomodoro?",
     "opts": [("Not likely",0),("Maybe",1),("Likely",2),("Definitely",3)]}
]

# Max score = 60
psych_states = {
    "Very Low Usage": (0, 10),
    "Low Usage": (11, 20),
    "Moderate Usage": (21, 35),
    "High Usage": (36, 50),
    "Very High Usage": (51, 60)
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Pomodoro Survey")
st.title("🍅 Pomodoro Technique Survey")

st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

if st.button("Start Survey"):

    errors = []
    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed below.")

        total_score = 0
        answers = []

        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            score = next(score for label, score in q["opts"] if label == choice)
            total_score += score

            answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score
            })

        status = interpret_score(total_score)

        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"Total Score: {total_score} / 60")

        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": answers,
            "version": version_float
        }

        json_filename = f"{sid}_pomodoro_result.json"
        save_json(json_filename, record)

        st.success(f"Saved as {json_filename}")
        st.download_button("Download JSON", json.dumps(record, indent=2), file_name=json_filename)