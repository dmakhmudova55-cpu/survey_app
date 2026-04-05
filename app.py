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
]

# Max score = sum of max option scores
psych_states = {
    "Very Low Usage": (0, 3),
    "Low Usage": (4, 6),
    "Moderate Usage": (7, 9),
    "High Usage": (10, 11),
    "Very High Usage": (12, 12)
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

# --- Form for survey ---
with st.form("pomodoro_form"):
    name = st.text_input("Given Name")
    surname = st.text_input("Surname")
    dob = st.text_input("Date of Birth (YYYY-MM-DD)")
    sid = st.text_input("Student ID (digits only)")

    # Display questions
    answers = []
    for idx, q in enumerate(questions):
        choice = st.selectbox(f"Q{idx+1}. {q['q']}", [opt[0] for opt in q["opts"]], key=f"q{idx}")
        answers.append(choice)

    submitted = st.form_submit_button("Submit Survey")

if submitted:
    # --- Validate user inputs ---
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
        # --- Calculate total score ---
        total_score = 0
        answer_records = []
        for idx, q in enumerate(questions):
            selected = answers[idx]
            score = next(score for label, score in q["opts"] if label == selected)
            total_score += score
            answer_records.append({"question": q["q"], "selected_option": selected, "score": score})

        # --- Interpret score ---
        status = interpret_score(total_score)
        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"Total Score: {total_score} / {len(questions)*3}")

        # --- Save JSON record ---
        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": answer_records,
            "version": version_float
        }

        json_filename = f"{sid}_pomodoro_result.json"
        save_json(json_filename, record)
        st.success(f"Saved as {json_filename}")
        st.download_button("Download JSON", json.dumps(record, indent=2), file_name=json_filename)