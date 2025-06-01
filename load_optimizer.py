EFFORT_SCORES = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}

def generate_schedule(task_list, work_start="09:00", work_end="17:00", break_every=90):
    from datetime import datetime, timedelta
    import pandas as pd

    # Convert input times
    fmt = "%H:%M"
    current_time = datetime.strptime(work_start, fmt)
    end_time = datetime.strptime(work_end, fmt)

    schedule = []
    task_list_sorted = sorted(
        task_list,
        key=lambda x: (EFFORT_SCORES[x["Effort"]], -x["Duration (min)"]),
        reverse=True
    )

    time_since_break = 0

    for task in task_list_sorted:
        duration = int(task["Duration (min)"])
        if current_time + timedelta(minutes=duration) > end_time:
            break

        if time_since_break >= break_every:
            schedule.append({
                "Start": current_time.strftime(fmt),
                "End": (current_time + timedelta(minutes=15)).strftime(fmt),
                "Task": "Break"
            })
            current_time += timedelta(minutes=15)
            time_since_break = 0

        schedule.append({
            "Start": current_time.strftime(fmt),
            "End": (current_time + timedelta(minutes=duration)).strftime(fmt),
            "Task": task["Task"]
        })

        current_time += timedelta(minutes=duration)
        time_since_break += duration

    return pd.DataFrame(schedule)

def compute_energy_profile(schedule_df, task_list):
    import pandas as pd

    EFFORT_IMPACT = {
        "High": 30,
        "Medium": 20,
        "Low": 10
    }

    energy = 100
    timeline = []

    for _, row in schedule_df.iterrows():
        task = row["Task"]

        if task == "Break":
            energy = min(100, energy + 10)
        else:
            effort = next((t["Effort"] for t in task_list if t["Task"] == task), "Low")
            duration_minutes = pd.to_datetime(row["End"]) - pd.to_datetime(row["Start"])
            duration_hours = duration_minutes.total_seconds() / 3600
            energy -= EFFORT_IMPACT[effort] * duration_hours

        energy = max(0, energy)
        timeline.append({"Time": row["End"], "Energy": energy})

    return pd.DataFrame(timeline)
