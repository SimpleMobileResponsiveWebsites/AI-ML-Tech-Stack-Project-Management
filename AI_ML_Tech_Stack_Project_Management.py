import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize Data
FRAMEWORKS = [
    "TensorFlow", "PyTorch", "Scikit-learn", "XGBoost",
    "Hugging Face Transformers", "LangChain",
    "NumPy", "Pandas", "Matplotlib", "Seaborn"
]

# Page Configuration
st.set_page_config(page_title="AI/ML Project Management", layout="wide")

# Sidebar
st.sidebar.title("Project Management")
selected_framework = st.sidebar.selectbox("Select Framework", FRAMEWORKS)
task_filter = st.sidebar.selectbox("Task Status Filter", ["All", "Pending", "In Progress", "Completed"])
st.sidebar.write("---")
st.sidebar.header("Quick Actions")
reset_data = st.sidebar.button("Reset Data")

# State Initialization
if "tasks" not in st.session_state or reset_data:
    st.session_state.tasks = pd.DataFrame(columns=["Framework", "Task", "Status", "Due Date", "Notes"])

# Main Page
st.title("AI/ML Tech Stack Project Management")

# Add a new task
st.header("Add a New Task")
with st.form("task_form"):
    task_name = st.text_input("Task Name", "")
    task_status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])
    task_due_date = st.date_input("Due Date", datetime.now())
    task_notes = st.text_area("Notes", "")
    submitted = st.form_submit_button("Add Task")

if submitted and task_name:
    new_task = {
        "Framework": selected_framework,
        "Task": task_name,
        "Status": task_status,
        "Due Date": task_due_date,
        "Notes": task_notes,
    }
    st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_task])], ignore_index=True)
    st.success("Task added successfully!")

# Display Tasks
st.header("Task Overview")

# Filter tasks based on the selected task filter
if task_filter == "All":
    filtered_tasks = st.session_state.tasks
else:
    filtered_tasks = st.session_state.tasks[
        st.session_state.tasks["Status"].str.contains(task_filter, case=False, na=False)
    ]

if not filtered_tasks.empty:
    st.dataframe(filtered_tasks, use_container_width=True)
else:
    st.write(f"No tasks available for the filter: {task_filter}.")

# Notes Section
st.header("Project Notes")
project_notes = st.text_area("Document your thoughts or ideas here.", "")
if st.button("Save Notes"):
    with open("project_notes.txt", "a") as f:
        f.write(f"\n[{datetime.now()}]\n{project_notes}\n")
    st.success("Notes saved successfully!")
