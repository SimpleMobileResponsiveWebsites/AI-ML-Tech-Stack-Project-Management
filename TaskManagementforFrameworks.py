import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize completely empty DataFrame
empty_data = {
    "Framework": [],
    "Task": [],
    "Status": [],
    "Due Date": [],
    "Notes": []
}

# Initialize session state if it doesn't exist
if 'tasks_df' not in st.session_state:
    st.session_state.tasks_df = pd.DataFrame(empty_data)

# Page Configuration
st.set_page_config(page_title="AI/ML Project Management", layout="wide")

# Sidebar Task Selection (only shown when tasks exist)
st.sidebar.header("Task Navigation")
if not st.session_state.tasks_df.empty:
    selected_task = st.sidebar.selectbox(
        "Select Task to View",
        options=st.session_state.tasks_df.index,
        format_func=lambda x: f"{st.session_state.tasks_df.loc[x, 'Framework']} - {st.session_state.tasks_df.loc[x, 'Task']}"
    )
else:
    st.sidebar.write("No tasks available yet. Add your first task using the form below!")

# Additional Sidebar Filters (only shown when tasks exist)
if not st.session_state.tasks_df.empty:
    st.sidebar.header("Task Filters")
    framework_filter = st.sidebar.multiselect(
        "Filter by Framework",
        options=st.session_state.tasks_df["Framework"].unique()
    )
    status_filter = st.sidebar.multiselect(
        "Filter by Status",
        options=["Pending", "In Progress", "Completed"]
    )

# Reset Data Button
st.sidebar.write("---")
st.sidebar.header("Quick Actions")
if st.sidebar.button("Reset Data"):
    st.session_state.tasks_df = pd.DataFrame(empty_data)
    st.success("All tasks have been cleared.")

# Main Page
st.title("AI/ML Tech Stack Project Management")

# Task Addition Section
st.header("Add a New Task")
with st.form("add_task_form"):
    framework = st.selectbox(
        "Framework", 
        options=[
            "PyTorch", "TensorFlow", "Scikit-learn", "XGBoost",
            "Hugging Face Transformers", "LangChain",
            "NumPy", "Pandas", "Matplotlib", "Seaborn"
        ]
    )
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
    st.session_state.tasks_df = pd.concat(
        [st.session_state.tasks_df, pd.DataFrame([new_task])],
        ignore_index=True
    )
    st.success("New task added successfully!")

# Display Tasks Overview
st.header("Tasks Overview")
if not st.session_state.tasks_df.empty:
    # Apply filters if they exist
    filtered_df = st.session_state.tasks_df.copy()
    if 'framework_filter' in locals() and framework_filter:
        filtered_df = filtered_df[filtered_df["Framework"].isin(framework_filter)]
    if 'status_filter' in locals() and status_filter:
        filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]
    
    # Display filtered tasks
    if not filtered_df.empty:
        for idx, row in filtered_df.iterrows():
            with st.expander(
                f"{row['Framework']} - {row['Task']}", 
                expanded=(idx == selected_task if 'selected_task' in locals() else False)
            ):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Status:** {row['Status']}")
                    st.write(f"**Due Date:** {row['Due Date']}")
                    st.write(f"**Notes:** {row['Notes']}")
                
                with col2:
                    new_status = st.selectbox(
                        "Update Status",
                        options=["Pending", "In Progress", "Completed"],
                        index=["Pending", "In Progress", "Completed"].index(row["Status"]),
                        key=f"status_{idx}"
                    )
                    if st.button(f"Update Task", key=f"update_{idx}"):
                        st.session_state.tasks_df.at[idx, "Status"] = new_status
                        st.success(f"Task status updated to {new_status}!")
                        st.experimental_rerun()
    else:
        st.info("No tasks match the selected filters. Try adjusting your filters or add a new task.")
else:
    st.info("👋 Welcome! No tasks available yet. Get started by adding your first task using the form above.")

# Project Notes Section
st.header("Project Notes")
project_notes = st.text_area("Document your thoughts or ideas here.", "")
if st.button("Save Notes"):
    with open("project_notes.txt", "a") as f:
        f.write(f"\n[{datetime.now()}]\n{project_notes}\n")
    st.success("Notes saved successfully!")

# Download Button (only shown when tasks exist)
if not st.session_state.tasks_df.empty:
    st.download_button(
        label="Download Tasks",
        data=st.session_state.tasks_df.to_csv(index=False),
        file_name="tasks.csv",
        mime="text/csv",
    )
