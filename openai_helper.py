import openai
import os
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def break_down_task(task_description):
    prompt = (
        f"Break the following task into 3 to 5 clear, actionable subtasks:\n"
        f"Task: {task_description}\n"
        f"Subtasks:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        output = response.choices[0].message.content
        subtasks = [line.strip("-•. ") for line in output.splitlines() if line.strip()]
        return subtasks

    except openai.RateLimitError:
        return "QUOTA_EXCEEDED"

    except Exception as e:
        return f"ERROR: {str(e)}"
