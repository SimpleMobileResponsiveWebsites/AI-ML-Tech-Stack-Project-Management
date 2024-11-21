import streamlit as st
import pandas as pd
from datetime import datetime

# Sample data as a DataFrame
data = {
    "Framework": [
        "PyTorch", "TensorFlow", "Scikit-learn", "XGBoost", "Hugging Face Transformers",
        "LangChain", "NumPy", "Pandas", "Matplotlib", "Seaborn"
    ],
    "Task": ["setup development environment"] * 10,
    "Status": ["Pending"] * 10,
    "Due Date": ["2024-11-21"] * 10,
    "Notes": [
        "I want to setup a test development environment for PyTorch using PyCharm Professional 2023.3.3"
    ] * 10,
}
tasks_df = pd.DataFrame(data)

# Page Configuration
st.set_page_config(page_title="Task Management for Frameworks", layout="wide")

# Sidebar Filters
st.sidebar.header("Task Filters")
framework_filter = st.sidebar.multiselect("Filter by Framework", options=tasks_df["Framework"].unique())
status_filter = st.sidebar.multiselect("Filter by Status", options=tasks_df["Status"].unique())

# Filter DataFrame based on Sidebar Inputs
filtered_df = tasks_df
if framework_filter:
    filtered_df = filtered_df[filtered_df["Framework"].isin(framework_filter)]
if status_filter:
    filtered_df = filtered_df[filtered_df["Status"].isin(status_filter)]

# Main Page
st.title("Framework Task Management")

# Display tasks
st.header("Tasks Overview")
if not filtered_df.empty:
    for idx, row in filtered_df.iterrows():
        with st.expander(f"{row['Framework']} - {row['Task']}"):
            st.write(f"**Status:** {row['Status']}")
            st.write(f"**Due Date:** {row['Due Date']}")
            st.write(f"**Notes:** {row['Notes']}")
            
            # Update task status
            new_status = st.selectbox(
                "Update Status",
                options=["Pending", "In Progress", "Completed"],
                index=["Pending", "In Progress", "Completed"].index(row["Status"]),
                key=f"status_{idx}"
            )
            if st.button(f"Update Task {idx}", key=f"update_{idx}"):
                tasks_df.at[idx, "Status"] = new_status
                st.success(f"Task status updated to {new_status}!")
else:
    st.write("No tasks match the selected filters.")

# Task Addition Section
st.header("Add a New Task")
with st.form("add_task_form"):
    framework = st.selectbox("Framework", options=tasks_df["Framework"].unique())
    task_name = st.text_input("Task Name", "")
    status = st.selectbox("Status", options=["Pending", "In Progress", "Completed"])
    due_date = st.date_input("Due Date", datetime.now())
    notes = st.text_area("Notes", "")
    submitted = st.form_submit_button("Add Task")

if submitted:
    new_task = {
        "Framework": framework,
        "Task": task_name,
        "Status": status,
        "Due Date": due_date.strftime("%Y-%m-%d"),
        "Notes": notes,
    }
    tasks_df = pd.concat([tasks_df, pd.DataFrame([new_task])], ignore_index=True)
    st.success("New task added successfully!")

# Save Data
st.download_button(
    label="Download Updated Tasks",
    data=tasks_df.to_csv(index=False),
    file_name="updated_tasks.csv",
    mime="text/csv",
)
