import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="AI/ML Project Management", layout="wide")

# Sidebar - Task Selector
st.sidebar.header("Task Management")
st.sidebar.write("---")
st.sidebar.header("Quick Actions")
reset_data = st.sidebar.button("Reset Data")

# Initialize Data if Reset or Session Empty
if "tasks" not in st.session_state or reset_data:
    st.session_state.tasks = pd.DataFrame(columns=["Framework", "Task", "Status", "Due Date", "Notes"])
    st.success("Data has been reset.")

# Sidebar Filters
st.sidebar.write("---")
if not st.session_state.tasks.empty:
    selected_task = st.sidebar.selectbox(
        "Select Task", 
        st.session_state.tasks["Task"].unique(), 
        key="task_selector"
    )
else:
    selected_task = None

# Main Page
st.title("AI/ML Tech Stack Project Management")

# Add a New Task Section
st.header("Add a New Task")
with st.form("add_task_form"):
    framework = st.selectbox("Framework", options=[
        "PyTorch", "TensorFlow", "Scikit-learn", "XGBoost",
        "Hugging Face Transformers", "LangChain",
        "NumPy", "Pandas", "Matplotlib", "Seaborn"
    ])
    task_name = st.text_input("Task Name", "")
    status = st.selectbox("Status", options=["Pending", "In Progress", "Completed"])
    due_date = st.date_input("Due Date", datetime.now())
    notes = st.text_area("Notes", "")
    submitted = st.form_submit_button("Add Task")

if submitted and task_name:
    new_task = {
        "Framework": framework,
        "Task": task_name,
        "Status": status,
        "Due Date": due_date.strftime("%Y-%m-%d"),
        "Notes": notes,
    }
    st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_task])], ignore_index=True)
    st.success("New task added successfully!")

# Display Tasks Section
st.header("Tasks Overview")
if not st.session_state.tasks.empty:
    if selected_task:
        task_details = st.session_state.tasks[st.session_state.tasks["Task"] == selected_task]
        for _, row in task_details.iterrows():
            with st.expander(f"{row['Framework']} - {row['Task']}"):
                st.write(f"**Framework:** {row['Framework']}")
                st.write(f"**Status:** {row['Status']}")
                st.write(f"**Due Date:** {row['Due Date']}")
                st.write(f"**Notes:** {row['Notes']}")
                # Update task status
                new_status = st.selectbox(
                    "Update Status",
                    options=["Pending", "In Progress", "Completed"],
                    index=["Pending", "In Progress", "Completed"].index(row["Status"]),
                    key=f"status_{row.name}"
                )
                if st.button(f"Update Task {row.name}", key=f"update_{row.name}"):
                    st.session_state.tasks.at[row.name, "Status"] = new_status
                    st.success(f"Task status updated to {new_status}!")
    else:
        st.write("Select a task from the sidebar to view details.")
else:
    st.write("No tasks available.")

# Notes Section
st.header("Project Notes")
project_notes = st.text_area("Document your thoughts or ideas here.", "")
if st.button("Save Notes"):
    with open("project_notes.txt", "a") as f:
        f.write(f"\n[{datetime.now()}]\n{project_notes}\n")
    st.success("Notes saved successfully!")

# Save Data
if not st.session_state.tasks.empty:
    st.download_button(
        label="Download Updated Tasks",
        data=st.session_state.tasks.to_csv(index=False),
        file_name="updated_tasks.csv",
        mime="text/csv",
    )
