import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cognitive Load Manager", layout="centered")

st.title("🧠 Cognitive Load Manager")
st.write("Plan your tasks based on mental effort and optimize your productivity.")

# Initialize session state for persistent task storage
if "task_list" not in st.session_state:
    st.session_state.task_list = []

st.subheader("📌 Add a New Task")

# Task input fields
task_name = st.text_input("Task Name")
effort_level = st.selectbox("Effort Level", ["High", "Medium", "Low"])
duration = st.number_input("Estimated Duration (minutes)", min_value=1, max_value=240)
priority = st.selectbox("Priority (optional)", ["None", "Low", "Medium", "High"])

# Add task button
if st.button("➕ Add Task"):
    if task_name.strip() == "":
        st.warning("⚠️ Task name cannot be empty.")
    else:
        st.session_state.task_list.append({
            "Task": task_name,
            "Effort": effort_level,
            "Duration (min)": duration,
            "Priority": priority
        })
        st.success(f"✅ Added task: {task_name}")

# Display current task list
if st.session_state.task_list:
    st.subheader("📝 Task List")
    st.dataframe(pd.DataFrame(st.session_state.task_list))

# Display task table if there are tasks
if st.session_state.task_list:
    st.subheader("📝 Task List")
    st.dataframe(pd.DataFrame(st.session_state.task_list))

if st.button("🗑️ Clear All Tasks"):
    st.session_state.task_list = []
    st.success("All tasks cleared.")

if st.session_state.task_list:
    df = pd.DataFrame(st.session_state.task_list)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Tasks", csv, "tasks.csv", "text/csv")

