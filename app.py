import streamlit as st
import pandas as pd
from load_optimizer import generate_schedule, compute_energy_profile

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

    df = pd.DataFrame(st.session_state.task_list)
    st.dataframe(df)

    # Layout buttons side by side
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Clear All Tasks"):
            st.session_state.task_list = []
            st.success("All tasks cleared.")

    with col2:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Tasks", csv, "tasks.csv", "text/csv")

from openai_helper import break_down_task

if st.session_state.task_list:
    st.subheader("🧩 Break a Task Into Subtasks")

    task_names = [task["Task"] for task in st.session_state.task_list]
    task_to_break = st.selectbox("Select a task to break down", task_names)

    if st.button("🔍 Break Down Task"):
        with st.spinner("Thinking..."):
            subtasks = break_down_task(task_to_break)

        st.success("Here are your subtasks:")
        for sub in subtasks:
            st.write(f"• {sub}")

        if st.button("➕ Add Subtasks to Schedule"):
            for sub in subtasks:
                st.session_state.task_list.append({
                    "Task": sub,
                    "Effort": "Medium",
                    "Duration (min)": 30,
                    "Priority": "None"
                })
            st.success("Subtasks added to your list.")

from load_optimizer import generate_schedule

st.subheader("⚙️ Schedule Settings")

col1, col2, col3 = st.columns(3)

with col1:
    work_start = st.time_input("Start Time", value=pd.to_datetime("09:00").time())

with col2:
    work_end = st.time_input("End Time", value=pd.to_datetime("17:00").time())

with col3:
    break_every = st.number_input("Break Interval (mins)", min_value=30, max_value=180, value=90, step=15)

st.caption("⏰ Your schedule will be optimized within your selected work hours and break preferences.")

if st.session_state.task_list:
    st.subheader("📆 Suggested Daily Schedule")

    schedule_df = generate_schedule(
    st.session_state.task_list,
    work_start=work_start.strftime("%H:%M"),
    work_end=work_end.strftime("%H:%M"),
    break_every=break_every
)

    st.dataframe(schedule_df)

from load_optimizer import compute_energy_profile
import plotly.express as px

if st.session_state.task_list:
    energy_df = compute_energy_profile(schedule_df, st.session_state.task_list)
    st.subheader("🔋 Cognitive Load Battery")
    fig = px.area(energy_df, x="Time", y="Energy", range_y=[0, 100],
                  title="Mental Energy Depletion Over Time",
                  labels={"Time": "Time of Day", "Energy": "Remaining Cognitive Energy"})
    st.plotly_chart(fig, use_container_width=True)

if st.button("🔍 Break Down Task", key="break_task_button"):
    with st.spinner("Thinking..."):
        subtasks = break_down_task(task_to_break)

    if subtasks == "QUOTA_EXCEEDED":
        st.error("⚠️ You’ve exceeded your OpenAI usage quota. Please check your API plan or upgrade your account.")
    elif isinstance(subtasks, str) and subtasks.startswith("ERROR"):
        st.error(f"🚨 Something went wrong:\n\n{subtasks}")
    else:
        st.success("Here are your subtasks:")
        for sub in subtasks:
            st.write(f"• {sub}")

        if st.button("➕ Add Subtasks to Schedule"):
            for sub in subtasks:
                st.session_state.task_list.append({
                    "Task": sub,
                    "Effort": "Medium",
                    "Duration (min)": 30,
                    "Priority": "None"
                })
            st.success("Subtasks added to your list.")
